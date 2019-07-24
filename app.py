import json
from flask import Flask, render_template
import pandas as pd
import filesystem_lru
from application_integrity import IntegrityChecker
import non_essential_files

app = Flask(__name__)
#workspace = "/Dinesh/Genesys/designer/workspace/"



@app.route("/")
def index():
    """
    Home page 
    """
    chart_data = {}
    return chart_data

@app.route("/lru/<ccid>/")
@app.route("/lru/<ccid>/<top>/<days>/")
def fs_lru(ccid, top=None, days=None):
    if top == None:
        top = 100
    chart_data = filesystem_lru.get_top_lru(workspace + ccid, top=top, days=days)
    chart_data = json.dumps(chart_data, indent=2)
    return chart_data

@app.route("/checkintegrity/<ccid>")
def app_integrity(ccid):
    ic = IntegrityChecker(workspace, ccid)
    data = ic.validate_tenant_apps()
    data = json.dumps(data, indent=2)
    return data

@app.route("/nonessential/<ccid>")
def app_nonessential(ccid):
    nonEssentialJson = non_essential_files.non_essential_json(workspace, ccid)
    data = json.dumps(nonEssentialJson, indent=2)
    return data

@app.route("/nonessentialcount/<ccid>")
def app_nonessentialcount(ccid):
    nonEssentialJson = non_essential_files.non_essential_count(workspace, ccid)
    data = json.dumps(nonEssentialJson, indent=2)
    return data

@app.route("/nonessentialfiles/<ccid>")
def app_nonessentialfile(ccid):
    nonEssentialJson = non_essential_files.list_non_essential_files(workspace, ccid)
    data = json.dumps(nonEssentialJson, indent=2)
    return data

@app.route("/essentialfiles/<ccid>")
def app_essentialfile(ccid):
    nonEssentialJson = non_essential_files.list_essential_files(workspace, ccid)
    data = json.dumps(nonEssentialJson, indent=2)
    return data


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
