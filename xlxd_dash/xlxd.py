import os
import time
import re
from xlxd_dash import config

def xlxd_data():
    res = {}
    pid_file = config["xlxd"]["pidfile"]
    res["uptime"] = int(time.time() - os.path.getctime(pid_file))

    xml_file = config["xlxd"]["xml"]
    with open(xml_file) as f:
        contenido = f.read()

    res["version"] = 'N/A'
    match = re.search(r"<Version>(.*?)</Version>", contenido)
    if match:
        res["version"] = match.group(1)

    return res
