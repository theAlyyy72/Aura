import re
from datetime import datetime

import tools
from ml.intent import predict_intent

CONFIDENCE = 0.35


def handle(command):
    """Reply string dega, ya None agar LLM ko jawab dena hai."""
    command = command.lower().strip()
    intent, conf = predict_intent(command)
    print(f"[intent] {intent} ({conf:.2f})")

    if conf < CONFIDENCE or intent == "chat":
        return None

    if intent == "greeting":
        return "Hello! I am AURA, your personal assistant."
    if intent == "time":
        return datetime.now().strftime("The time is %I:%M %p.")
    if intent == "date":
        return datetime.now().strftime("Today's date is %d %B %Y.")
    if intent == "read_notes":
        return tools.read_notes()
    if intent == "total_expenses":
        return tools.total_expenses()

    if intent == "add_expense":
        m = re.search(r"(\d+(?:\.\d+)?)", command)
        if not m:
            return "I could not catch the amount. Please say it again, like add 200 rupees for lunch."
        tail = command[m.end():]
        c = re.search(r"\b(?:for|on|to)\s+(?:my\s+)?([a-z]+)", tail)
        return tools.add_expense(float(m.group(1)), c.group(1) if c else "general")

    if intent == "add_note":
        text = re.sub(
            r"^(please |can you )?(save|take|make|add|keep|write|put|note|remember|jot|remind me)"
            r"( down| a| the| this)*( note| reminder)?( that| to| about| of)?\s*",
            "", command).strip()
        return tools.add_note(text or command)

    if intent == "open_app":
        m = re.search(r"(?:open|launch|run|start|fire up)\s+(?:the\s+)?([a-z ]+?)(?:\s+app)?(?:\s+for me)?$", command)
        if not m:
            return "Which app should I open?"
        return tools.open_app(m.group(1).title())

    return None 