from xlxd_dash import config
import xmltodict
import re
from xlxd_common import (
    get_flag_info,
    mask_ip,
    normalize_xlxd_xml,
    parse_xlxd_datetime,
    read_xlxd_xml,
)

def xml_load():
    xml = read_xlxd_xml(config["xlxd"]["xml"])
    if not xml["available"]:
        return xml

    data = normalize_xlxd_xml(xml["xml"])
    data["available"] = True
    return data

def empty_data(message, detail=None):
    return {
        "available": False,
        "message": message,
        "detail": detail,
        "heard_users": [],
        "linked_nodes": [],
        "linked_peers": [],
    }

def json_load():
    xml = xml_load()
    if not xml["available"]:
        return empty_data(xml["message"], xml.get("detail"))

    heard_users = []
    linked_nodes = []
    linked_peers = []
    nodesIP = config["service"]["nodesIP"]
    peersIP = config["service"]["peersIP"]

    try:
        data = xmltodict.parse(xml["data"], force_list=("STATION", "NODE"))
        num = 1
        key = f"{xml['name']}_heard_users"
        if key in data["DATA"] and data["DATA"][key] and "STATION" in data["DATA"][key]:
            for station in data["DATA"][key]["STATION"]:
                temp = station
                parts = station["Callsign"].split("/")
                temp["Call"] = parts[0].strip()
                temp["CallLink"] = temp["Call"].split()[0]

                temp["Suffix"] = parts[1].strip() if len(parts) > 1 else ""
                temp["Flag"] = get_flag_info(temp["Call"])

                temp["Via_node"] = re.sub(r"\s+", "-", temp["Via_node"].strip())

                temp["LastHeardTime"] = parse_xlxd_datetime(temp["LastHeardTime"])

                heard_users.append(temp)
                num += 1

        num = 1
        key = f"{xml['name']}_linked_nodes"
        if key in data["DATA"] and data["DATA"][key] and "NODE" in data["DATA"][key]:
            for node in data["DATA"][key]["NODE"]:
                temp = node

                temp["Flag"] = get_flag_info(temp["Callsign"])

                temp["Callsign"] = re.sub(r"\s+", "-", temp["Callsign"].strip())

                temp["ConnectTime"] = parse_xlxd_datetime(temp["ConnectTime"])
                temp["LastHeardTime"] = parse_xlxd_datetime(temp["LastHeardTime"])

                temp["IP"] = mask_ip(temp["IP"], nodesIP)

                linked_nodes.append(temp)
                num += 1

        key = f"{xml['name']}_linked_peers"
        if key in data["DATA"] and data["DATA"][key] and "PEER" in data["DATA"][key]:
            for peer in data["DATA"][key]["PEER"]:
                temp = peer

                temp["ConnectTime"] = parse_xlxd_datetime(temp["ConnectTime"])
                temp["LastHeardTime"] = parse_xlxd_datetime(temp["LastHeardTime"])

                temp["IP"] = mask_ip(temp["IP"], peersIP)

                linked_peers.append(temp)
                num += 1

        data["NAME"] = xml["name"]
        return {"available": True,
                "message": "",
                "heard_users": sorted(heard_users, key=lambda x: x["LastHeardTime"], reverse=True),
                "linked_nodes": sorted(linked_nodes, key=lambda x: x["LastHeardTime"], reverse=True),
                "linked_peers": sorted(linked_peers, key=lambda x: x["LastHeardTime"], reverse=True),
                }
    except Exception as e:
        print(f"Error processing XML file: {e}")
        return empty_data("XLXD data could not be processed.", str(e))
