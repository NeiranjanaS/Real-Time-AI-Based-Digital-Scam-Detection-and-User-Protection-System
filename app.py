from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import json

from qr_detector import scan_qr
from phishing_model import calculate_risk

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
HISTORY_FILE = "history.json"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------- HOME ----------
@app.route("/")
def home():
    return render_template("index.html")

# ---------- STAGE 1 : URL ----------
@app.route("/scan_url")
def scan_url():
    return render_template("scan_url.html")

@app.route("/check_url", methods=["POST"])
def check_url():
    url = request.form["url"]

    risk, status, reasons = calculate_risk(url)

    # Save history
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)

    history.append({
        "type": "URL",
        "content": url,
        "risk": risk,
        "status": status
    })

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

    return render_template(
        "result.html",
        result=url,
        risk=risk,
        status=status,
        reasons=reasons
    )

# ---------- STAGE 2 : QR ----------
@app.route("/qr_scan")
def qr_scan():
    return render_template("qr_scan.html")

@app.route("/scan_qr", methods=["POST"])
def scan_qr_route():

    if "qrimage" not in request.files:
        return "No File Uploaded"

    file = request.files["qrimage"]

    if file.filename == "":
        return "No File Selected"

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    file.save(filepath)

    qr_data = scan_qr(filepath)

    if qr_data is None:
        return render_template(
            "result.html",
            result="QR NOT DETECTED",
            risk=0,
            status="INVALID",
            reasons=["No QR Code Found."]
        )

    risk, status, reasons = calculate_risk(qr_data)

    # Save QR history
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)

    history.append({
        "type": "QR",
        "content": qr_data,
        "risk": risk,
        "status": status
    })

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

    return render_template(
        "result.html",
        result=qr_data,
        risk=risk,
        status=status,
        reasons=reasons
    )

# ---------- HISTORY ----------
@app.route("/history")
def history():

    history = []

    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)

    history.reverse()

    return render_template("history.html", history=history)

if __name__ == "__main__":
    app.run(debug=True)