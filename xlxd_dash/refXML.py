from xlxd_dash import config
import xmltodict
import json
import os
import requests
import time
from lxml import etree
from xlxd_common import as_list, is_online, safe_int

sd = os.path.dirname(os.path.abspath(__file__))

def ref_xml():
    url = f"{config['xlxd']['apiURL']}?do=GetReflectorList"
    try:
        response = requests.get(url, timeout=10)
    except Exception as e:
        print(f"Error getting reflector list: {e}")
        return False

    if response.status_code == 200:
        xml_str = response.content.decode("utf-8")
        return xml_str

    return False

def sanitize_xml(xml_str):
    parser = etree.XMLParser(recover=True)
    try:
        root = etree.fromstring(xml_str.encode("utf-8"), parser=parser)
        return etree.tostring(root, encoding="utf-8").decode("utf-8")
    except Exception as e:
        print(f"❌ Error sanitizando XML: {e}")
        return xml_str  # fallback sin modificar

def ref_json():
    usar_cache = False
    CACHE_PATH = "/tmp/ref_cache.json"
    CACHE_TTL = config["xlxd"].get("ref_cache_ttl", 60)

    if os.path.exists(CACHE_PATH):
        mtime = os.path.getmtime(CACHE_PATH)
        if time.time() - mtime < CACHE_TTL:
            usar_cache = True

    if usar_cache:
        try:
            with open(CACHE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"Error reading reflector cache: {e}")
            usar_cache = False

    if not usar_cache:
        xml = ref_xml()
        if not xml:
            return {}  # o lanzar excepción si preferís
        xml = sanitize_xml(xml)
        data = xmltodict.parse(xml)
        with open(CACHE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f)

    return data

def ref_list():
    data = ref_json()
    reflectors = data.get("XLXAPI", {}) \
                     .get("answer", {}) \
                     .get("reflectorlist", {}) \
                     .get("reflector", [])
    now = int(time.time())
    offline_time = config["xlxd"].get("offline_time", 2400)

    items = []
    for reflector in as_list(reflectors):
        item = dict(reflector)
        item["lastcontact"] = safe_int(item.get("lastcontact"))
        item["online"] = is_online(item["lastcontact"], now, offline_time)
        items.append(item)

    return {
        "available": bool(items),
        "message": "" if items else "Reflector list is not available.",
        "reflectors": items,
    }

def get_ref(ref_id):
    ref_id = ref_id.upper()

    for item in ref_list()["reflectors"]:
        if item.get("name", "").upper() == ref_id:
            return item

    return None
