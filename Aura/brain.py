import json
import os
from dotenv import load_dotenv
from openai import OpenAI
import tools

load_dotenv()
client = OpenAI()
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

SYSTEM_PROMPT = (
    "You are AURA, a friendly voice assistant. "
    "Reply in one or two short sentences in plain text, "
    "no markdown or lists, because your answer is spoken aloud. "
    "Use the available tools when the user asks to save notes, "
    "read notes, track expenses, or open apps."
)

TOOLS = [
    {"type": "function", "function": {
        "name": "add_note",
        "description": "Save a note for the user",
        "parameters": {"type": "object",
                       "properties": {"text": {"type": "string"}},
                       "required": ["text"]}}},
    {"type": "function", "function": {
        "name": "read_notes",
        "description": "Read the user's latest saved notes",
        "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {
        "name": "add_expense",
        "description": "Record an expense in rupees",
        "parameters": {"type": "object",
                       "properties": {"amount": {"type": "number"},
                                      "category": {"type": "string"}},
                       "required": ["amount", "category"]}}},
    {"type": "function", "function": {
        "name": "total_expenses",
        "description": "Get the total of all recorded expenses",
        "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {
        "name": "open_app",
        "description": "Open an application on the Mac, e.g. Calculator, Safari",
        "parameters": {"type": "object",
                       "properties": {"name": {"type": "string"}},
                       "required": ["name"]}}},
]

AVAILABLE = {
    "add_note": tools.add_note,
    "read_notes": tools.read_notes,
    "add_expense": tools.add_expense,
    "total_expenses": tools.total_expenses,
    "open_app": tools.open_app,
}

history = [{"role": "system", "content": SYSTEM_PROMPT}]


def trim_history():
    while len(history) > 21:
        del history[1]
    while len(history) > 1 and history[1]["role"] != "user":
        del history[1]


def run_tool(call):
    name = call.function.name
    try:
        args = json.loads(call.function.arguments or "{}")
        result = AVAILABLE[name](**args)
    except Exception as e:
        result = f"Tool error: {e}"
    print(f"[tool] {name} -> {result}")
    return result


def ask_llm(user_text):
    start = len(history)
    history.append({"role": "user", "content": user_text})
    trim_history()
    try:
        for _ in range(4):
            response = client.chat.completions.create(
                model=MODEL, messages=history, tools=TOOLS
            )
            msg = response.choices[0].message

            if not msg.tool_calls:
                reply = (msg.content or "").strip()
                history.append({"role": "assistant", "content": reply})
                return reply

            history.append({
                "role": "assistant",
                "content": msg.content,
                "tool_calls": [
                    {"id": c.id, "type": "function",
                     "function": {"name": c.function.name,
                                  "arguments": c.function.arguments}}
                    for c in msg.tool_calls
                ],
            })
            for call in msg.tool_calls:
                history.append({"role": "tool",
                                "tool_call_id": call.id,
                                "content": run_tool(call)})
    except Exception as e:
        print("LLM error:", e)
        del history[start:]
        return "Sorry, I am having trouble thinking right now."

    return "Sorry, I could not finish that."