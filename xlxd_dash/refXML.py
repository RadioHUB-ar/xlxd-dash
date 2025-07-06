from xlxd_dash import config
import xmltodict
import json
import os
from datetime import datetime
import requests
import time
from lxml import etree

sd = os.path.dirname(os.path.abspath(__file__))

with open(f"{sd}/callprefix.json") as f:
    callprefix = json.load(f)

def ref_xml():
    url = f"{config['xlxd']['apiURL']}?do=GetReflectorList"
    response = requests.get(url)

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
    CACHE_TTL = 600

    if os.path.exists(CACHE_PATH):
        mtime = os.path.getmtime(CACHE_PATH)
        if time.time() - mtime < CACHE_TTL:
            usar_cache = True

    if usar_cache:
        with open(CACHE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        xml = ref_xml()
        if not xml:
            return {}  # o lanzar excepción si preferís
        xml = sanitize_xml(xml)
        data = xmltodict.parse(xml)
        with open(CACHE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f)

    return data

