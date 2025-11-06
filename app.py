from flask import Flask, render_template_string
import pandas as pd
import os

app = Flask(__name__)

TEMPLATE = """
<!doctype html>
<title>EchelonID Reports</title>
<h1>EchelonID – IGA Reports</h1>
<p>Generated from local Python scripts (lifecycle, policy, PKI)</p>
{% for name, table in tables %}
  <h2>{{ name }}</h2>
  {{ table|safe }}
{% endfor %}
"""

@app.route("/")
def index():
    tables = []
    if os.path.exists("output/access_review_report.csv"):
        df = pd.read_csv("output/access_review_report.csv")
        tables.append(("Access Review Report", df.to_html(index=False)))
    if os.path.exists("output/policy_alignment_report.csv"):
        df = pd.read_csv("output/policy_alignment_report.csv")
        tables.append(("Policy Alignment Report", df.to_html(index=False)))
    if os.path.exists("output/expired_certs_report.csv"):
        df = pd.read_csv("output/expired_certs_report.csv")
        tables.append(("PKI Expiry Report", df.to_html(index=False)))
    return render_template_string(TEMPLATE, tables=tables)

if __name__ == "__main__":
    app.run(debug=True)
