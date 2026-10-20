import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

SYSTEM_PROMPT = (
    "You are AURA, a friendly voice assistant. "
    "Reply in one or two short sentences in plain text, "
    "no markdown or lists, because your answer is spoken aloud."
)

history = [{"role": "system", "content": SYSTEM_PROMPT}]


def ask_llm(user_text):
    history.append({"role": "user", "content": user_text})
    try:
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[history[0]] + history[-10:],
        )
        reply = response.choices[0].message.content.strip()
    except Exception as e:
        print("LLM error:", e)
        history.pop()
        return "Sorry, I am having trouble thinking right now."

    history.append({"role": "assistant", "content": reply})
    return reply
