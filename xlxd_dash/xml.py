from xlxd_dash import config
import xmltodict
import re
import json
import os
from datetime import datetime

sd = os.path.dirname(os.path.abspath(__file__))
with open(f"{sd}/callprefix.json") as f:
    callprefix = json.load(f)

def xml_load():
    ref_name = ''
    xml_file = config["xlxd"]["xml"]
    with open(xml_file, "r", encoding="utf-8") as f:
        XML = f.read()

    # Extraer el encabezado XML
    match = re.match(r'(<\?xml.*?\?>)', XML)
    header = match.group(1) if match else ""

    # Extraer el nombre del ref
    ref_match = re.search(r"<(XLX[\w\d]{3}) ", XML)
    if ref_match:
        ref_name = ref_match.group(1)

    # Eliminar el encabezado del XML para limpiarlo
    XML = XML[len(header):].strip()

    # **Reemplazar etiquetas con espacios por `_`**
    XML = re.sub(r"<([\w]+)\s+([\w\s]+)>", lambda m: f"<{m.group(1)}_{m.group(2).replace(' ', '_')}>", XML)
    XML = re.sub(r"</([\w]+)\s+([\w\s]+)>", lambda m: f"</{m.group(1)}_{m.group(2).replace(' ', '_')}>", XML)

    # Envolver el XML en una etiqueta raíz para evitar errores
    XML = f"<DATA>\n{XML}\n</DATA>"

    return { "name": ref_name, "data": XML }

def call_flag(codigo_pais):
    return ''.join(chr(0x1F1E6 + ord(letra) - ord('A')) for letra in codigo_pais.upper())

def get_flag(distintiva):
    """Busca el mejor match reduciendo la distintiva hasta encontrar un prefijo válido."""
    while distintiva:
        if distintiva in callprefix:
            return [ call_flag(callprefix[distintiva][0]), callprefix[distintiva][1]]
        distintiva = distintiva[:-1]
    return ""

def json_load():
    xml = xml_load()
    data = xmltodict.parse(xml["data"])
    heard_users = {}
    linked_nodes = {}

    num = 1
    for station in data["DATA"][f"{xml["name"]}_heard_users"]["STATION"]:
        temp = station
        parts = station["Callsign"].split("/")
        temp["Call"] = parts[0].strip()
        temp["Suffix"] = parts[1].strip() if len(parts) > 1 else ""
        temp["Flag"] = get_flag(temp["Call"])

        fecha_str = temp["LastHeardTime"]
        fecha_obj = datetime.strptime(fecha_str, "%A %a %b %d %H:%M:%S %Y")
        temp["LastHeardTime"] = int(fecha_obj.timestamp())

        heard_users[num] = temp
        num += 1

    num = 1
    for node in data["DATA"][f"{xml["name"]}_linked_nodes"]["NODE"]:
        temp = node

        temp["Flag"] = get_flag(temp["Callsign"])

        fecha_str = temp["ConnectTime"]
        fecha_obj = datetime.strptime(fecha_str, "%A %a %b %d %H:%M:%S %Y")
        temp["ConnectTime"] = int(fecha_obj.timestamp())

        fecha_str = temp["LastHeardTime"]
        fecha_obj = datetime.strptime(fecha_str, "%A %a %b %d %H:%M:%S %Y")
        temp["LastHeardTime"] = int(fecha_obj.timestamp())

        linked_nodes[num] = temp
        num += 1

    data["NAME"] = xml["name"]
    return { "heard_users": heard_users,  "linked_nodes": linked_nodes}
