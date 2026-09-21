import re

# Simple AI-based URL Risk Analyzer
def analyze_url(url):

    risk = 0
    reasons = []

    # HTTPS Check
    if not url.startswith("https://"):
        risk += 20
        reasons.append("Website is not using HTTPS.")

    # Long URL
    if len(url) > 50:
        risk += 15
        reasons.append("URL is unusually long.")

    # @ Symbol
    if "@" in url:
        risk += 20
        reasons.append("URL contains '@' symbol.")

    # IP Address
    ip_pattern = r"(\\d{1,3}\\.){3}\\d{1,3}"
    if re.search(ip_pattern, url):
        risk += 25
        reasons.append("Website uses an IP address instead of a domain.")

    # Suspicious Keywords
    keywords = [
        "login","verify","secure","bank",
        "account","update","free","gift",
        "otp","payment"
    ]

    for word in keywords:
        if word in url.lower():
            risk += 5
            reasons.append(f"Suspicious keyword detected: {word}")

    # Many Dashes
    if url.count("-") >= 3:
        risk += 10
        reasons.append("Too many '-' characters.")

    # Final Classification
    if risk >= 60:
        status = "🔴 Phishing Website"
    elif risk >= 30:
        status = "🟡 Suspicious Website"
    else:
        status = "🟢 Safe Website"

    return {
        "risk": min(risk,100),
        "status": status,
        "reasons": reasons
    }