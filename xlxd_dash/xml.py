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

    match = re.match(r'(<\?xml.*?\?>)', XML)
    header = match.group(1) if match else ""

    ref_match = re.search(r"<(XLX[\w\d]{3}) ", XML)
    if ref_match:
        ref_name = ref_match.group(1)

    XML = XML[len(header):].strip()

    XML = re.sub(r"<([\w]+)\s+([\w\s]+)>", lambda m: f"<{m.group(1)}_{m.group(2).replace(' ', '_')}>", XML)
    XML = re.sub(r"</([\w]+)\s+([\w\s]+)>", lambda m: f"</{m.group(1)}_{m.group(2).replace(' ', '_')}>", XML)

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

def maskIP(ip, mask):
    if mask == 0:
        return False
    return ".".join(ip.split(".")[:mask] + ["?"] * (4 - mask))

def json_load():
    xml = xml_load()
    data = xmltodict.parse(xml["data"], force_list=("STATION", "NODE"))
    heard_users = []
    linked_nodes = []
    linked_peers = []
    nodesIP = config["service"]["nodesIP"]
    peersIP = config["service"]["peersIP"]

    try:
        num = 1
        key = f"{xml['name']}_heard_users"
        if key in data["DATA"] and data["DATA"][key] and "STATION" in data["DATA"][key]:
            for station in data["DATA"][key]["STATION"]:
                temp = station
                parts = station["Callsign"].split("/")
                temp["Call"] = parts[0].strip()
                temp["CallLink"] = temp["Call"].split()[0]

                temp["Suffix"] = parts[1].strip() if len(parts) > 1 else ""
                temp["Flag"] = get_flag(temp["Call"])

                temp["Via_node"] = re.sub(r"\s+", "-", temp["Via_node"].strip())

                fecha_str = temp["LastHeardTime"]
                fecha_obj = datetime.strptime(fecha_str, "%A %a %b %d %H:%M:%S %Y")
                temp["LastHeardTime"] = int(fecha_obj.timestamp())

                heard_users.append(temp)
                num += 1

        num = 1
        key = f"{xml['name']}_linked_nodes"
        if key in data["DATA"] and data["DATA"][key] and "NODE" in data["DATA"][key]:
            for node in data["DATA"][key]["NODE"]:
                temp = node

                temp["Flag"] = get_flag(temp["Callsign"])

                temp["Callsign"] = re.sub(r"\s+", "-", temp["Callsign"].strip())

                fecha_str = temp["ConnectTime"]
                fecha_obj = datetime.strptime(fecha_str, "%A %a %b %d %H:%M:%S %Y")
                temp["ConnectTime"] = int(fecha_obj.timestamp())

                fecha_str = temp["LastHeardTime"]
                fecha_obj = datetime.strptime(fecha_str, "%A %a %b %d %H:%M:%S %Y")
                temp["LastHeardTime"] = int(fecha_obj.timestamp())

                temp["IP"] = maskIP(temp["IP"], nodesIP)

                linked_nodes.append(temp)
                num += 1

        key = f"{xml['name']}_linked_peers"
        if key in data["DATA"] and data["DATA"][key] and "PEER" in data["DATA"][key]:
            for peer in data["DATA"][key]["PEER"]:
                temp = peer

                fecha_str = temp["ConnectTime"]
                fecha_obj = datetime.strptime(fecha_str, "%A %a %b %d %H:%M:%S %Y")
                temp["ConnectTime"] = int(fecha_obj.timestamp())

                fecha_str = temp["LastHeardTime"]
                fecha_obj = datetime.strptime(fecha_str, "%A %a %b %d %H:%M:%S %Y")
                temp["LastHeardTime"] = int(fecha_obj.timestamp())

                temp["IP"] = maskIP(temp["IP"], peersIP)

                linked_peers.append(temp)
                num += 1

        data["NAME"] = xml["name"]
        return {"heard_users": sorted(heard_users, key=lambda x: x["LastHeardTime"], reverse=True),
                "linked_nodes": sorted(linked_nodes, key=lambda x: x["LastHeardTime"], reverse=True),
                "linked_peers": sorted(linked_peers, key=lambda x: x["LastHeardTime"], reverse=True),
                }
    except Exception as e:
        print(f"Error processing XML file: {e}")
        return {}