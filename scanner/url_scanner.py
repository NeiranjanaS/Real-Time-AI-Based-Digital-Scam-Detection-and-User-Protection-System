import joblib
import re
import os

MODEL_PATH = "models/url_model.pkl"

# Load trained model
model = joblib.load(MODEL_PATH)


def phishing_reasons(url):

    reasons = []

    if not url.startswith("https://"):
        reasons.append("Website does not use HTTPS.")

    if len(url) > 70:
        reasons.append("URL length is unusually long.")

    if url.count(".") > 3:
        reasons.append("Too many subdomains detected.")

    if "-" in url:
        reasons.append("Hyphen found in domain name.")

    if "@" in url:
        reasons.append("@ symbol detected.")

    suspicious = [
        "login","verify","bank","secure","update","free",
        "gift","otp","wallet","payment","signin","account"
    ]

    for word in suspicious:
        if word in url.lower():
            reasons.append(f"Suspicious keyword detected: {word}")

    if len(reasons) == 0:
        reasons.append("No suspicious phishing indicators detected.")

    return reasons


def scan_url(url):

    clean = re.sub(r"https?://", "", url.lower())

    prediction = model.predict([clean])[0]

    probability = model.predict_proba([clean])[0]

    confidence = round(max(probability) * 100, 2)

    if str(prediction).lower() in {"1", "phishing", "scam"}:
        label = "Scam"
    else:
        label = "Safe"

    return {
        "prediction": label,
        "confidence": confidence,
        "reasons": phishing_reasons(url)
    }