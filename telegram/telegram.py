import time
import xml.etree.ElementTree as ET
import re
import requests
import json
import os
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading
import traceback

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from xlxd_common import get_flag, normalize_xlxd_xml, parse_xlxd_datetime, read_xlxd_xml

ref_name = ""
with open(os.path.join(PROJECT_ROOT, "config_tg.json"), "r", encoding="utf-8") as f:
    config = json.load(f)

modules = config["service"]["modules"]
user_online = config["service"]["user_online"]
user_gap = config["service"]["user_gap"] * 60
node_online = config["service"]["node_online"]
node_offline = config["service"]["node_offline"] * 60
node_delay = config["service"]["node_delay"]
logger = config["service"]["logger"]
xml_file = config["xlxd"]["xml"]
TG_URL = f"https://api.telegram.org/bot{config['service']['token']}/sendMessage"

dt_format = "%A %a %b %d %H:%M:%S %Y"

nodes_old = {}
nodes_off = {}
stations_old = {}

notif = []
process = False

timer = None

def send_message(msg, dest):
    for CHAT_ID in dest:
        while True:
            data = {"chat_id": CHAT_ID, "text": msg}
            try:
                res = requests.post(TG_URL, data=data, timeout=10)
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(5)
                continue

            if res.status_code == 200:
                break

            print(f"Error HTTP {res.status_code}. Reintentando…")
            time.sleep(5)

def split_node_callsign(callsign):
    parts = callsign.split(maxsplit=1)
    if len(parts) == 2:
        return parts[0], parts[1]
    return callsign, ""

def format_node_call(call, initial):
    return f"{call}-{initial}" if initial else call

def load_xml():
    xml = read_xlxd_xml(xml_file)
    if not xml["available"]:
        return xml

    data = normalize_xlxd_xml(xml["xml"], root_name="ROOT")
    data["available"] = True
    return data

def analizar_xml():
    global nodes_old, stations_old, notif, process, nodes_off, ref_name
    now = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    now_epoch = int(time.time())
    try:
        xml = load_xml()
        if not xml["available"]:
            send_message(xml["message"], logger)
            return False

        ref_name = xml["name"]
        XML = xml["data"]

        if not process:
            send_message(f"REF: {ref_name}", logger)

        root = ET.fromstring(XML)

        ### NODES - Armar lista de nodos actualmente vistos en el XML (nodes_now)
        nodes_now = {}
        for node in root.findall(".//NODE"):
            callsign = (node.findtext("Callsign") or "").strip()
            call, initial = split_node_callsign(callsign)
            ip = (node.findtext("IP") or "").strip()
            linked_module = (node.findtext("LinkedModule") or "").strip()
            protocol = (node.findtext("Protocol") or "").strip()
            connect_time = (node.findtext("ConnectTime") or "").strip()
            last_heard_time = (node.findtext("LastHeardTime") or "").strip()

            connect_time_epoch = parse_xlxd_datetime(connect_time)
            last_heard_time_epoch = parse_xlxd_datetime(last_heard_time)

            index = (callsign + "-" + protocol or "").strip().replace(' ','_')
            if index in nodes_now.keys():
                if nodes_now[index]["ConnectTime_epoch"] < connect_time_epoch:
                    nodes_now[index] = {
                        "Callsign": callsign,
                        "Call": call,
                        "Initial": initial,
                        "IP": ip,
                        "LinkedModule": linked_module,
                        "Protocol": protocol,
                        "ConnectTime": connect_time,
                        "ConnectTime_epoch": connect_time_epoch,
                        "LastHeardTime": last_heard_time,
                        "LastHeardTime_epoch": last_heard_time_epoch
                    }
            else:
                nodes_now[index] = {
                    "Callsign": callsign,
                    "Call": call,
                    "Initial": initial,
                    "IP": ip,
                    "LinkedModule": linked_module,
                    "Protocol": protocol,
                    "ConnectTime": connect_time,
                    "ConnectTime_epoch": connect_time_epoch,
                    "LastHeardTime": last_heard_time,
                    "LastHeardTime_epoch": last_heard_time_epoch
                }

        ### NODES - Si NO es la primer corrida (process = True) y veo diferencias, guardo los json de nodes_now y nodes_old
        if process:
            ### NODES - si hay nuevos (now - old)
            nuevos = nodes_now.keys() - nodes_old.keys()
            if nuevos:
                for key in nuevos:
                    Call = nodes_now[key]["Call"]
                    Initial = nodes_now[key]["Initial"]
                    NodeCall = format_node_call(Call, Initial)
                    LinkedModule = nodes_now[key]["LinkedModule"]
                    Protocol = nodes_now[key]["Protocol"]
                    flag = get_flag(Call)
                    if key in nodes_off.keys():
                        del nodes_off[key]
                        send_message(f"Online {NodeCall} On {ref_name} {LinkedModule} Protocol {Protocol}", logger)
                    else:
                        if (LinkedModule in modules):
                            notifto = logger + node_offline
                        else:
                            notifto = logger

                        send_message(f"✅{flag} {NodeCall} On {ref_name} {LinkedModule} Protocol {Protocol}", notifto)

            ### NODES - si faltan nodes que antes estaban (old - now)
            eliminados = nodes_old.keys() - nodes_now.keys()
            if eliminados:
                for key in eliminados:
                    Call = nodes_old[key]["Call"]
                    Initial = nodes_old[key]["Initial"]
                    NodeCall = format_node_call(Call, Initial)
                    LinkedModule = nodes_old[key]["LinkedModule"]
                    Protocol = nodes_old[key]["Protocol"]
                    send_message(f"Offline {NodeCall} From {ref_name} {LinkedModule} Protocol {Protocol}", logger)
                    nodes_off[key] = nodes_old[key]
                    nodes_off[key]["last_off"] = now_epoch

            for key in list(nodes_off.keys()):
                if nodes_off[key]["last_off"] + node_delay < now_epoch:
                    Call = nodes_off[key]["Call"]
                    Initial = nodes_off[key]["Initial"]
                    NodeCall = format_node_call(Call, Initial)
                    LinkedModule = nodes_off[key]["LinkedModule"]
                    Protocol = nodes_off[key]["Protocol"]
                    flag = get_flag(Call)
                    if (LinkedModule in modules):
                        notifto = logger + node_offline
                    else:
                        notifto = logger
                    send_message(f"❌{flag} {NodeCall} From {ref_name} {LinkedModule} Protocol {Protocol}", notifto)
    
                    del nodes_off[key]

        nodes_old = nodes_now

        stations_now = {}
        for station in root.findall(".//STATION"):
            callsign = (station.findtext("Callsign") or "").strip()
            if "/" in callsign:
                call, id = map(str.strip, callsign.split("/", maxsplit=1))
            else:
                call = callsign.strip()
                id = ""
            via_node = (station.findtext("Via_node") or "").strip()
            on_module = (station.findtext("On_module") or "").strip()
            via_peer = (station.findtext("Via_peer") or "").strip()
            last_heard_time = (station.findtext("LastHeardTime") or "").strip()

            last_heard_time_epoch = parse_xlxd_datetime(last_heard_time)

            index = (callsign or "").strip().replace(' ', '_')

            if index in stations_now.keys():
                if stations_now[index]["LastHeardTime_epoch"] < last_heard_time_epoch:
                    stations_now[index] = {
                        "Callsign": callsign,
                        "Call": call,
                        "ID": id,
                        "Via_node": via_node,
                        "On_module": on_module,
                        "Via_peer": via_peer,
                        "LastHeardTime": last_heard_time,
                        "LastHeardTime_epoch": last_heard_time_epoch
                    }
            else:
                stations_now[index] = {
                    "Callsign": callsign,
                    "Call": call,
                    "ID": id,
                    "Via_node": via_node,
                    "On_module": on_module,
                    "Via_peer": via_peer,
                    "LastHeardTime": last_heard_time,
                    "LastHeardTime_epoch": last_heard_time_epoch
                }

        if process:
            for item in stations_now.keys():
                ID = stations_now[item]["ID"]
                if ID:
                    Call = stations_now[item]["Call"]+" / "+ID
                else:
                    Call = stations_now[item]["Call"]
                Via_node = re.sub(r"\s+", "-", stations_now[item]["Via_node"])
                On_module = stations_now[item]["On_module"]
                flag = get_flag(stations_now[item]["Call"])

                if (On_module in modules):
                    notifto = logger + user_online
                else:
                    notifto = logger

                if item not in stations_old.keys():
                    send_message(f"🗣{flag} {Call} Via {Via_node} On {ref_name} {On_module}", notifto)
                else:
                    if stations_old[item]["LastHeardTime_epoch"] + user_gap < stations_now[item]["LastHeardTime_epoch"]:
                        send_message(f"🗣{flag} {Call} Via {Via_node} On {ref_name} {On_module}", notifto)

        stations_old = stations_now

        return True

    except FileNotFoundError:
        send_message(f"Error: No se encontró el archivo {xml_file}", logger)
        return False
    except ET.ParseError as e:
        send_message(f"Error procesando XML: {e}", logger)
        return False
    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        trace = "\n".join(traceback.format_list(tb))
        send_message(f"{e}\n{trace}", logger)
        return False

class XMLmonitor(FileSystemEventHandler):
    def on_modified(self, event):
        global timer
        if event.src_path == xml_file:
            if timer:
                timer.cancel()
            timer = threading.Timer(1.0, analizar_xml)
            timer.start()

def INITmonitor():
    event_handler = XMLmonitor()
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(xml_file), recursive=False)  # Monitorea solo la carpeta
    observer.start()
    send_message(f"Iniciando monitoreo de {xml_file}...", logger)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()

if __name__ == "__main__":
    while True:
        process = analizar_xml()
        if process:
            INITmonitor()
        else:
            time.sleep(30)
