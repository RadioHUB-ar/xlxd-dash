import requests
import random
from flask import Response
from xlxd_dash import config, save_config
from xlxd_dash.xlxd import xlxd_data
import re

def do_callhome():
    print("Calling home...")
    xlxd = xlxd_data()
    if "ip" in config["service"]:
        refIP = config["service"]["ip"]
    else:
        refIP = requests.get("https://ifconfig.me").text

    if "hash" not in config["xlxd"]:
        chars = "1234567890abcdefghijklmnopqrstuvwyxzABCDEFGHIJKLMNAOPQRSTUVWYXZ"
        config["xlxd"]["hash"] = ''.join(random.choices(chars, k=16))
        save_config()

    reflector = f"""
  <name>{config["service"]["name"]}</name>
  <uptime>{xlxd["uptime"]}</uptime>
  <hash>{config["xlxd"]["hash"]}</hash>
  <url>{config["service"]["dashURL"]}</url>
  <country>{config["service"]["country"]}</country>
  <comment>{config["service"]["comment"]}</comment>
  <ip>{refIP}</ip>
  <reflectorversion>{xlxd["version"]}</reflectorversion>
"""

    xml = f"""<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>
<query>CallingHome</query>
<reflector>
{reflector}
</reflector>
<interlinks>
</interlinks>"""

    try:
        response = requests.post(
            config["xlxd"]["apiURL"],
            data={"xml": xml},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )

        match = re.search(r"<timestamp>(.*?)</timestamp>", response.text)
        if match:
            config["xlxd"]["last_callhome"] = match.group(1)
            save_config()
            print("Callhome response:")
            print(response.text)

        return Response(response.text, status=response.status_code, mimetype="text/plain")
    except Exception as e:
        print("Callhome error: {e}")
        return Response(f"Error en callhome: {e}", status=500)
