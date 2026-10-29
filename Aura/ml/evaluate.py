from pathlib import Path

import joblib
from sklearn.metrics import accuracy_score, classification_report

model = joblib.load(Path(__file__).parent / "intent_model.joblib")

FRESH_TEST = [
    ("remind me to renew my passport", "add_note"),
    ("make a note that the rent is due on friday", "add_note"),
    ("jot this down call the plumber tomorrow", "add_note"),
    ("can you save a reminder to buy groceries", "add_note"),
    ("write that I need to finish the report", "add_note"),
    ("what did I tell you to remember earlier", "read_notes"),
    ("can you read my saved notes", "read_notes"),
    ("do I have any reminders", "read_notes"),
    ("tell me what is in my notes", "read_notes"),
    ("I paid 350 for petrol today", "add_expense"),
    ("put 75 rupees under snacks", "add_expense"),
    ("note that I spent 1200 on groceries", "add_expense"),
    ("at rs 200 for lunch", "add_expense"),
    ("add 90 rupees for auto fare", "add_expense"),
    ("how much money have I spent this month", "total_expenses"),
    ("what is the sum of all my expenses", "total_expenses"),
    ("give me the total of my spending", "total_expenses"),
    ("tell me how much I have spent so far", "total_expenses"),
    ("open Spotify for me", "open_app"),
    ("can you launch Notes", "open_app"),
    ("start Safari now", "open_app"),
    ("open the Calendar app", "open_app"),
    ("tell me what time it is right now", "time"),
    ("what's the time", "time"),
    ("could you check the time for me", "time"),
    ("can you tell me today's date", "date"),
    ("what's today's date", "date"),
    ("I forgot the date, what is it", "date"),
    ("good evening aura", "greeting"),
    ("hey aura good morning", "greeting"),
    ("namaste aura", "greeting"),
    ("what is the weather like in mumbai", "chat"),
    ("explain what a database index is", "chat"),
    ("who is the prime minister of india", "chat"),
    ("tell me a short story about a robot", "chat"),
    ("how can I improve my sleep", "chat"),
    ("what is a good movie to watch tonight", "chat"),
    ("what is the difference between a list and a tuple", "chat"),
    ("give me a fun fact about octopuses", "chat"),
    ("how do I prepare for a coding interview", "chat"),
]

X = [t.lower() for t, _ in FRESH_TEST]
y_true = [y for _, y in FRESH_TEST]
y_pred = model.predict(X)

correct = sum(a == b for a, b in zip(y_true, y_pred))
print(f"Fresh test accuracy: {accuracy_score(y_true, y_pred):.2%} ({correct}/{len(y_true)})\n")
print(classification_report(y_true, y_pred, zero_division=0))
print("Mistakes:")
for t, a, b in zip(X, y_true, y_pred):
    if a != b:
        print(f"  '{t}' -> predicted {b}, expected {a}")