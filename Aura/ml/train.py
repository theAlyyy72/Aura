from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.pipeline import make_pipeline

HERE = Path(__file__).parent

HAND_TEST = [
    ("remind me to call the dentist", "add_note"),
    ("jot down pick up the parcel", "add_note"),
    ("make a note about the project deadline", "add_note"),
    ("read back what I told you to remember", "read_notes"),
    ("do I have any saved notes", "read_notes"),
    ("tell me my notes", "read_notes"),
    ("I paid 80 for coffee", "add_expense"),
    ("put 300 on groceries", "add_expense"),
    ("note an expense of 450 for petrol", "add_expense"),
    ("how much money did I spend in total", "total_expenses"),
    ("give me my spending total", "total_expenses"),
    ("what have I spent so far", "total_expenses"),
    ("bring up Spotify", "open_app"),
    ("start Chrome please", "open_app"),
    ("I want to use the Calculator", "open_app"),
    ("what's the time right now", "time"),
    ("do you know what time it is", "time"),
    ("time please", "time"),
    ("what day is it today", "date"),
    ("tell me today's date", "date"),
    ("what is the date today", "date"),
    ("yo aura", "greeting"),
    ("good evening", "greeting"),
    ("hello there", "greeting"),
    ("do you like music", "chat"),
    ("what is the speed of light", "chat"),
    ("recommend a movie for tonight", "chat"),
    ("explain gradient descent briefly", "chat"),
    ("how do I stay focused", "chat"),
]

df = pd.read_csv(HERE / "intents.csv")

model = make_pipeline(
    TfidfVectorizer(ngram_range=(1, 2), lowercase=True),
    LogisticRegression(max_iter=1000, class_weight="balanced", C=10),
)
model.fit(df["text"], df["intent"])

X_test = [t.lower() for t, _ in HAND_TEST]
y_true = [y for _, y in HAND_TEST]
y_pred = model.predict(X_test)

print(f"Training examples: {len(df)}")
print(f"Hand-written test accuracy: {accuracy_score(y_true, y_pred):.2%}\n")
print(classification_report(y_true, y_pred, zero_division=0))

labels = sorted(set(y_true))
print("Confusion matrix (rows = true, cols = predicted):")
print(labels)
print(confusion_matrix(y_true, y_pred, labels=labels))

print("\nMistakes:")
for text, true, pred in zip(X_test, y_true, y_pred):
    if true != pred:
        print(f"  '{text}' -> predicted {pred}, expected {true}")

joblib.dump(model, HERE / "intent_model.joblib")
print("\nModel saved.")