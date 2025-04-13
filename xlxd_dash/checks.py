from .callhome import do_callhome
import re
from pathlib import Path
from xlxd_dash import config

def run_checks():
    print("Running checks...")
    if not bool(re.fullmatch(r"XLX[A-Z0-9]{3}", config["service"]["name"])):
        raise SystemExit(f"XLX name not set or invalid\nCheck GitHub page for more information.")

    checkfiles = [
        config["xlxd"]["pidfile"],
        config["xlxd"]["xml"],
    ]
    for file in checkfiles:
        if not Path(file).exists():
            raise SystemExit(f"Error reading file {file}\nCheck GitHub page for more information.")

    if config["xlxd"]["callhome"] == True:
        print("Startup callhome...")
        do_callhome()

    print("Checks completed successfully")
