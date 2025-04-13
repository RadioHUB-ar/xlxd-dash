from flask import Flask
import json

app = Flask(__name__)
dash_version = "0.9b"

with open("config.json") as f:
    config = json.load(f)

def save_config():
    with open("config.json", "w") as f:
        json.dump(config, f, indent=2)

from .checks import run_checks
run_checks()

from xlxd_dash import routes