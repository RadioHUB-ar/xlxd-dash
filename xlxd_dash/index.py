from flask import render_template
from xlxd_dash.xlxd import xlxd_data
from xlxd_dash import dash_version, config

def index():
    data = xlxd_data()
    return render_template("index.html",
                           name = config["service"]["name"],
                           country = config["service"]["country"],
                           comment = config["service"]["comment"],
                           author = config["service"]["author"],
                           footer = config["service"]["footer"],
                           uptime =  data["uptime"],
                           version = data["version"],
                           dash_version = dash_version,
                           description = config["service"]["description"],
                           keywords = config["service"]["description"],
                           links = config["service"]["links"]
                           )
