import subprocess
import sys 
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)
NOTES_FILE = DATA_DIR / "notes.txt"
EXPENSES_FILE = DATA_DIR / "expenses.txt"


def add_note(text):
    with open(NOTES_FILE, "a") as f:
        f.write(f"{datetime.now():%Y-%m-%d %H:%M} | {text}\n")
    return "Note saved."


def read_notes():
    if not NOTES_FILE.exists():
        return "You have no notes yet."
    lines = NOTES_FILE.read_text().strip().splitlines()
    if not lines:
        return "You have no notes yet."
    notes = [line.split(" | ", 1)[1] for line in lines[-5:]]
    return "Your latest notes: " + "; ".join(notes)


def add_expense(amount, category):
    with open(EXPENSES_FILE, "a") as f:
        f.write(f"{datetime.now():%Y-%m-%d} | {amount} | {category}\n")
    return f"Added {amount} rupees for {category}."


def total_expenses():
    if not EXPENSES_FILE.exists():
        return "No expenses yet."
    total = 0.0
    for line in EXPENSES_FILE.read_text().strip().splitlines():
        total += float(line.split(" | ")[1])
    return f"Your total expenses are {total:g} rupees."


def open_app(name):
    if sys.platform != "darwin":
        return "I can only open apps when i run on a mac."
    result = subprocess.run(["open","a", name], capture_output=True)
    if result.returncode == 0:
        return f"Opened {name}."
    return f"I could not find an app called {name}."