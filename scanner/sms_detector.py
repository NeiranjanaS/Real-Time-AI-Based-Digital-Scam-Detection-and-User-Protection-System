import joblib

model = joblib.load("models/sms_model.pkl")
vectorizer = joblib.load("models/sms_vectorizer.pkl")

keywords = [
    "otp","bank","free","winner","lottery",
    "gift","account","verify","payment","urgent"
]

def predict_sms(message):

    vector = vectorizer.transform([message])

    prediction = model.predict(vector)[0]
    probability = model.predict_proba(vector)[0]

    confidence = round(max(probability) * 100,2)

    reasons=[]

    for word in keywords:
        if word in message.lower():
            reasons.append(f"Suspicious keyword detected: {word}")

    if len(reasons)==0:
        reasons.append("No suspicious scam keywords detected.")

    is_spam = str(prediction).strip().lower() in {
        "1", "spam", "scam", "phishing", "phish"
    }

    return {
        "prediction":"Scam" if is_spam else "Safe",
        "confidence":confidence,
        "reasons":reasons
    }