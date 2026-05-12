import json
import os
import re
import fcntl
from datetime import datetime


DT_FORMAT = "%A %a %b %d %H:%M:%S %Y"
CALLPREFIX_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "xlxd_dash", "callprefix.json")

with open(CALLPREFIX_PATH, "r", encoding="utf-8") as f:
    CALLPREFIX = json.load(f)


def read_xlxd_xml(xml_file):
    if not os.path.exists(xml_file):
        return {
            "available": False,
            "message": "XLXD data is not available yet.",
            "detail": f"XML file not found: {xml_file}",
        }

    try:
        with open(xml_file, "r", encoding="utf-8") as f:
            try:
                fcntl.flock(f, fcntl.LOCK_SH | fcntl.LOCK_NB)
            except BlockingIOError:
                return {
                    "available": False,
                    "message": "XLXD data is being updated.",
                    "detail": f"XML file is locked: {xml_file}",
                }

            return {"available": True, "xml": f.read()}
    except Exception as e:
        return {
            "available": False,
            "message": "XLXD data could not be read.",
            "detail": str(e),
        }


def normalize_xlxd_xml(xml_text, root_name="DATA"):
    ref_name = ""
    match = re.match(r"(<\?xml.*?\?>)", xml_text)
    header = match.group(1) if match else ""

    ref_match = re.search(r"<(XLX[\w\d]{3}) ", xml_text)
    if ref_match:
        ref_name = ref_match.group(1)

    xml_text = xml_text[len(header):].strip()
    xml_text = re.sub(
        r"<([\w]+)\s+([\w\s]+)>",
        lambda m: f"<{m.group(1)}_{m.group(2).replace(' ', '_')}>",
        xml_text,
    )
    xml_text = re.sub(
        r"</([\w]+)\s+([\w\s]+)>",
        lambda m: f"</{m.group(1)}_{m.group(2).replace(' ', '_')}>",
        xml_text,
    )

    return {"name": ref_name, "data": f"<{root_name}>\n{xml_text}\n</{root_name}>"}


def parse_xlxd_datetime(value):
    if not value:
        return 0
    return int(datetime.strptime(value, DT_FORMAT).timestamp())


def call_flag(country):
    return "".join(chr(0x1F1E6 + ord(letter) - ord("A")) for letter in country.upper())


def get_flag_info(callsign):
    while callsign:
        if callsign in CALLPREFIX:
            return [call_flag(CALLPREFIX[callsign][0]), CALLPREFIX[callsign][1]]
        callsign = callsign[:-1]
    return ["", ""]


def get_flag(callsign):
    return get_flag_info(callsign)[0]


def mask_ip(ip, mask):
    if mask == 0:
        return False
    return ".".join(ip.split(".")[:mask] + ["?"] * (4 - mask))


def as_list(value):
    if not value:
        return []
    if isinstance(value, list):
        return value
    return [value]


def safe_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def is_online(last_contact, now, offline_time):
    return safe_int(last_contact) > now - safe_int(offline_time, 2400)
