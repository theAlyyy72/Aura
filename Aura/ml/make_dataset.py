import csv
import random
from pathlib import Path

random.seed(42)
PER_INTENT = 30

cats = ["food", "lunch", "travel", "petrol", "groceries", "movie", "coffee", "rent"]
apps = ["Safari", "Calculator", "Notes", "Spotify", "Chrome", "Mail", "Calendar"]
things = ["buy milk", "call mom", "meeting at 5", "submit assignment",
          "pay electricity bill", "gym at 7", "book train tickets",
          "water the plants", "email the professor"]

templates = {
    "add_note": [
        "save a note {t}", "remember {t}", "note down {t}",
        "take a note that {t}", "write down {t}", "add a note to {t}",
        "keep a note about {t}", "make a note to {t}",
        "please remember to {t}", "don't let me forget to {t}",
        "put {t} in my notes", "save this reminder {t}",
    ],
    "read_notes": [
        "what are my notes", "read my notes", "show my notes",
        "what did I save", "read me my notes", "what notes do I have",
        "list my notes", "read out my saved notes",
        "what did I ask you to remember", "any notes saved",
        "play back my notes",
    ],
    "add_expense": [
        "add {n} rupees for {c}", "I spent {n} on {c}",
        "log {n} rupees {c} expense", "record {n} for {c}",
        "spent {n} rupees on {c}", "{n} rupees went to {c}",
        "track {n} rupees for {c}", "save an expense of {n} for {c}",
        "add {n} to my {c} expenses", "I just spent {n} rupees on {c}",
    ],
    "total_expenses": [
        "what is my total expense", "how much have I spent",
        "total spending", "tell me my total expenses",
        "what is my expense total", "sum up my expenses",
        "how much did I spend altogether", "what is my total spending",
        "show my expense total", "calculate my expenses",
    ],
    "open_app": [
        "open {a}", "launch {a}", "please open {a} app",
        "can you open {a}", "run {a}", "open the {a} app",
        "fire up {a}", "launch the {a} app for me",
    ],
    "time": [
        "what is the time", "what time is it", "tell me the time",
        "current time please", "time now", "can you tell me the time",
        "what is the current time", "tell me what time it is now",
        "how late is it", "check the time",
    ],
    "date": [
        "what is the date", "what is today's date", "tell me the date",
        "today's date please", "what's the date", "can you tell me the date",
        "what date is it", "tell me the current date",
        "which date is it today", "date please",
    ],
    "greeting": [
        "hello", "hi", "hey", "hey aura", "good morning", "hi there",
        "hello aura", "hi aura", "hey there", "good afternoon",
        "namaste", "what's up aura", "hello hello",
    ],
    "chat": [
        "what are you doing", "explain RAG in one line", "tell me a joke",
        "who invented the telephone", "give me a motivational quote",
        "how does a neural network learn", "what is the capital of France",
        "can you tell me what I am", "explain machine learning simply",
        "how are you feeling today", "suggest a good book", "what is AWS",
        "help me plan my day", "why is the sky blue",
        "tell me something interesting", "who won the world cup in 2018",
        "what is the difference between AI and ML",
        "how do I learn python faster", "write a short poem about rain",
        "what should I cook for dinner", "translate good night into spanish",
        "how far is the moon", "explain what an API is",
        "give me tips for a job interview", "how does the internet work",
        "what is a good workout routine", "tell me a fun fact about space",
        "why do we dream", "explain docker in simple words",
        "what is overfitting", "how do airplanes fly",
        "suggest a name for my dog", "what is the meaning of life",
        "tell me a riddle", "how many days are in a leap year",
        "what is the tallest mountain",
        "can you explain what a transformer is",
        "how do I get better at maths", "what makes a good resume",
    ],
}

rows = set()
for intent, temps in templates.items():
    pool = set()
    for _ in range(3000):
        t = random.choice(temps)
        text = t.format(
            t=random.choice(things),
            n=random.choice([50, 100, 150, 200, 250, 500, 1000]),
            c=random.choice(cats),
            a=random.choice(apps),
        )
        pool.add(text.lower())
        if len(pool) >= PER_INTENT:
            break
    rows |= {(x, intent) for x in pool}

rows = sorted(rows)
out = Path(__file__).parent / "intents.csv"
with open(out, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["text", "intent"])
    w.writerows(rows)

print(f"Saved {len(rows)} examples to {out}")