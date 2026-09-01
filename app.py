from flask import Flask, render_template, request

app = Flask(__name__)

# Home Page
@app.route("/")
def home():
    return render_template("index.html")

# URL Scan Page
@app.route("/scan-url", methods=["GET", "POST"])
def scan_url():

    if request.method == "POST":

        url = request.form["url"]

        # Temporary AI Prediction
        if "https" in url:
            prediction = "Safe Website"
            risk = "15%"
        else:
            prediction = "Phishing Website"
            risk = "92%"

        return render_template(
            "result.html",
            scanned_url=url,
            prediction=prediction,
            risk=risk
        )

    return render_template("scan_url.html")

# QR Scan Page
@app.route("/scan-qr")
def scan_qr():
    return render_template("qr_scan.html")

# History Page
@app.route("/history")
def history():
    return render_template("history.html")

if __name__ == "__main__":
    app.run(debug=True)