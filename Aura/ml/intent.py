from pathlib import Path

import joblib

MODEL = joblib.load(Path(__file__).parent / "intent_model.joblib")


def predict_intent(text):
    probs = MODEL.predict_proba([text.lower()])[0]
    i = probs.argmax()
    return MODEL.classes_[i], float(probs[i])