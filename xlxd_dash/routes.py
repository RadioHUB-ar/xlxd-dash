from flask import request, send_from_directory, Response, render_template
from xlxd_dash import app
from xlxd_dash.callhome import do_callhome
from xlxd_dash.xml import json_load
from xlxd_dash.xlxd import xlxd_data
from xlxd_dash import dash_version, config
from xlxd_dash.refXML import ref_json

@app.route("/index.php")
@app.route("/")
def root():
    if "callhome" in request.args:
        return do_callhome()
    data = xlxd_data()
    return render_template('index.html',
                           css = [ 'main' ],
                           js = [ 'alpine', 'functions', 'index' ],
                           root = config['service']['dashURL'],
                           name = f"{config['service']['name']} - Dashboard",
                           country = config['service']['country'],
                           comment = config['service']['comment'],
                           author = config['service']['author'],
                           footer = config['service']['footer'],
                           uptime =  data['uptime'],
                           version = data['version'],
                           dash_version = dash_version,
                           description = config['service']['description'],
                           keywords = config['service']['description'],
                           links = config['service']['links'],
                           modules = config['service']['modules']
                           )

@app.route("/reflist")
def ref_list():
    return render_template('ref_list.html',
                           css = [ 'reflist' ],
                           js = [ 'alpine', 'functions', 'reflist' ],
                           root = config['service']['dashURL'],
                           name = f"{config['service']['name']} - Reflector List",
                           country = config['service']['country'],
                           comment = config['service']['comment'],
                           author = config['service']['author'],
                           footer = config['service']['footer'],
                           description = config['service']['description'],
                           keywords = config['service']['description'],
                           links = config['service']['links'],
                           modules = config['service']['modules'],
                           )

@app.route("/getreflist")
def get_ref_list():
    return ref_json()

@app.route("/get_data")
def get_data():
    return json_load()

@app.route("/xlxd_data")
def get_xlxd_data():
    return xlxd_data()

@app.route("/get_node")
def get_node():
    try:
        if request.is_json:
            params = request.get_json()
            call = params.get('call')
            proto = params.get('proto')
            if call and proto:
                data = json_load()
                linked_nodes = data["linked_nodes"]
                for entry in linked_nodes:
                    if entry.get("Callsign") == call and entry.get("Protocol") == proto:
                        return {"running": True}
    except:
        pass
    return {"running": False}

@app.route("/robots.txt")
def robots():
    return send_from_directory("static", "robots.txt")

@app.route("/sitemap.xml")
def sitemap():
    return send_from_directory("static", "sitemap.xml")

@app.route("/manifest.json")
def manifestjson():
    return Response(
        render_template("manifest.json.j2",
                        name=f"{config['service']['name']} Dashboard",
                        short_name=config["service"]["name"]),
                        mimetype="application/manifest+json"
    )