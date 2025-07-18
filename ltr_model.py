import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDRegressor
import joblib
import os

MODEL_PATH = "ltr_model.pkl"

def train_ltr_model(training_data):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(training_data["text"])
    y = training_data["feedback_score"]

    model = SGDRegressor(max_iter=1000, tol=1e-3)
    model.fit(X, y)

    joblib.dump((model, vectorizer), MODEL_PATH)
    return model, vectorizer

def load_ltr_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    return None, None

def predict_score(texts, model, vectorizer):
    if not model or not vectorizer:
        return [0.5] * len(texts)  # Neutral default score
    X = vectorizer.transform(texts)
    return model.predict(X)
