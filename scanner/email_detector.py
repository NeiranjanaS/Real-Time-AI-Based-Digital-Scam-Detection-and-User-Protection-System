import joblib

model = joblib.load("models/email_model.pkl")
vectorizer = joblib.load("models/email_vectorizer.pkl")

keywords = [
    "verify","password","account","login","bank",
    "payment","gift","reward","security","update"
]

def predict_email(text):

    vector = vectorizer.transform([text])

    prediction = model.predict(vector)[0]
    probability = model.predict_proba(vector)[0]

    confidence = round(max(probability)*100,2)

    reasons=[]

    for word in keywords:
        if word in text.lower():
            reasons.append(f"Suspicious keyword detected: {word}")

    if len(reasons)==0:
        reasons.append("Email appears legitimate.")

    is_phishing = str(prediction).strip().lower() in {
        "1", "phishing", "phish", "spam", "scam"
    }

    return {
        "prediction":"Scam" if is_phishing else "Safe",
        "confidence":confidence,
        "reasons":reasons
    }