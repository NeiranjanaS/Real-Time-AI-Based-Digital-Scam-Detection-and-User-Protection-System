import pandas as pd
import re
import joblib

from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

data = pd.read_csv("dataset/phishing_urls.csv")

data = data.dropna()

def preprocess(url):
    url = url.lower()
    url = re.sub(r"https?://", "", url)
    return url

data["url"] = data["url"].apply(preprocess)

X = data["url"]
y = data["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

pipeline = Pipeline([
    (
        "vectorizer",
        TfidfVectorizer(
            analyzer="char",
            ngram_range=(2,5)
        )
    ),
    (
        "classifier",
        RandomForestClassifier(
            n_estimators=200,
            random_state=42
        )
    )
])

pipeline.fit(X_train, y_train)

prediction = pipeline.predict(X_test)

print("Accuracy:", accuracy_score(y_test, prediction))
print(classification_report(y_test, prediction))

joblib.dump(pipeline, "models/url_model.pkl")

print("URL AI Model Saved Successfully")