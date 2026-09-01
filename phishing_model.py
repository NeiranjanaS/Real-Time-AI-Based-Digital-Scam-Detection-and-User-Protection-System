SAFE_DOMAINS = [
    "google.com",
    "amazon.in",
    "phonepe.com",
    "paytm.com",
    "gpay",
    "bharatpe"
]

def calculate_risk(data):

    risk = 0
    reasons = []

    data = data.lower()

    if data.startswith("http://"):
        risk += 30
        reasons.append("Website is not HTTPS secure.")

    if len(data) > 60:
        risk += 10
        reasons.append("Long URL detected.")

    short_urls = ["bit.ly","tinyurl","rb.gy","t.co"]

    for url in short_urls:
        if url in data:
            risk += 25
            reasons.append("Shortened URL detected.")

    keywords = [
        "login",
        "verify",
        "bank",
        "gift",
        "reward",
        "secure",
        "payment",
        "otp"
    ]

    for word in keywords:
        if word in data:
            risk += 10
            reasons.append(f"Suspicious keyword : {word}")

    trusted = False

    for domain in SAFE_DOMAINS:
        if domain in data:
            trusted = True

    if not trusted:
        risk += 20
        reasons.append("Unknown website domain.")

    if risk > 100:
        risk = 100

    if risk < 30:
        status = "SAFE"
    elif risk < 70:
        status = "SUSPICIOUS"
    else:
        status = "PHISHING"

    return risk, status, reasons