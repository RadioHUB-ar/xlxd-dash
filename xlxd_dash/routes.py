from flask import request, send_from_directory
from xlxd_dash import app
from xlxd_dash.callhome import do_callhome
from xlxd_dash.index import index
from xlxd_dash.xml import json_load

@app.route("/index.php")
@app.route("/")
def root():
    if "callhome" in request.args:
        return do_callhome()
    return index()

@app.route("/get_data")
def get_data():
    return json_load()

@app.route("/robots.txt")
def robots():
    return send_from_directory("static", "robots.txt")

@app.route("/sitemap.xml")
def sitemap():
    return send_from_directory("static", "sitemap.xml")