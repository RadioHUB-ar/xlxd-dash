import os
import time
import re
from xlxd_dash import config

def xlxd_data():
    res = {}
    res['running'] = False

    pid_file = config["xlxd"]["pidfile"]
    res["uptime"] = 0
    if os.path.exists(pid_file):
        res["uptime"] = int(time.time() - os.path.getctime(pid_file))

        with open(pid_file) as f:
            pid = f.read()

        try:
            os.kill(int(pid), 0)
            res['running'] = True
        except Exception as e:
            print(f"XLXD process check failed: {e}")

    xml_file = config["xlxd"]["xml"]
    res["version"] = 'N/A'
    if os.path.exists(xml_file):
        with open(xml_file) as f:
            contenido = f.read()

        match = re.search(r"<Version>(.*?)</Version>", contenido)
        if match:
            res["version"] = match.group(1)

    return res
