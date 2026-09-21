import pandas as pd
import joblib
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = PROJECT_ROOT / "dataset" / "phishing_emails.csv"
MODEL_DIR = PROJECT_ROOT / "models"

data = pd.read_csv(DATASET_PATH)

X = data["email"]
y = data["label"]

vectorizer = TfidfVectorizer(stop_words="english")

X_vec = vectorizer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_vec, y, test_size=0.2, random_state=42
)

model = MultinomialNB()

model.fit(X_train, y_train)

MODEL_DIR.mkdir(exist_ok=True)
joblib.dump(model, MODEL_DIR / "email_model.pkl")
joblib.dump(vectorizer, MODEL_DIR / "email_vectorizer.pkl")

print("Email Model Saved Successfully")