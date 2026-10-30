from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from brain import ask_llm
from router import handle

app = FastAPI(title="AURA API")


class ChatRequest(BaseModel):
    text: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
def chat(req: ChatRequest):
    text = req.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="text is empty")

    reply = handle(text)
    if reply is not None:
        return {"reply": reply, "source": "intent_model"}
    return {"reply": ask_llm(text), "source": "llm"}