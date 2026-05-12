from .callhome import do_callhome
import re
from pathlib import Path
from xlxd_dash import config

def run_checks():
    print("Running checks...")
    if not bool(re.fullmatch(r"XLX[A-Z0-9]{3}", config["service"]["name"])):
        raise SystemExit(f"XLX name not set or invalid\nCheck GitHub page for more information.")

    pid_file = config["xlxd"]["pidfile"]
    if not Path(pid_file).exists():
        print(f"Warning: PID file not found: {pid_file}")

    xml_file = config["xlxd"]["xml"]
    if not Path(xml_file).exists():
        print(f"Warning: XML file not found yet: {xml_file}")

    if config["xlxd"]["callhome"] == True:
        print("Startup callhome...")
        do_callhome()

    print("Checks completed successfully")
