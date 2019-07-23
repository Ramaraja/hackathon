import json
from flask import Flask, render_template
import pandas as pd
import filesystem_lru
from application_integrity import IntegrityChecker

app = Flask(__name__)
#workspace = "/Dinesh/Genesys/designer/workspace/"
workspace = "/ofs/"

@app.route("/")
def index():
    """
    Home page 
    """
    chart_data = {}
    return chart_data

@app.route("/lru")
def fs_lru():
    chart_data = filesystem_lru.get_top_lru("../00b392fd-c977-4be5-bf20-54c43a3a2a13")
    chart_data = json.dumps(chart_data, indent=2)
    return chart_data

@app.route("/checkintegrity/<ccid>")
def app_integrity(ccid):
    ic = IntegrityChecker(workspace, ccid)
    data = ic.validate_tenant_apps()
    data = json.dumps(data, indent=2)
    return data

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
