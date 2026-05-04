import ollama
import json
import re
from typing import Generator

SYSTEM_PROMPT = """
You are an intelligent inventory assistant for a company.
You have access to inventory data below.
Always respond in valid JSON format with this structure:
{
  "answer": "human-friendly explanation here",
  "data": [],
  "insight": "any useful observation",
  "confidence": "high | medium | low"
}
Never add text outside the JSON. Be conversational inside the answer field.
"""

def _build_messages(user_query: str, inventory_text: str):
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",   "content": f"INVENTORY DATA:\n{inventory_text}\n\nUSER QUESTION: {user_query}\n\nRespond ONLY in JSON."}
    ]

def ask(user_query: str, inventory_text: str) -> dict:
    """Non-streaming — full response at once."""
    response = ollama.chat(
        model="mistral",
        messages=_build_messages(user_query, inventory_text)
    )
    raw = response["message"]["content"]
    raw = re.sub(r"```json|```", "", raw).strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {
            "answer": raw,
            "data": [],
            "insight": "Could not parse structured JSON from model.",
            "confidence": "low"
        }

def ask_stream(user_query: str, inventory_text: str) -> Generator[str, None, None]:
    """Streaming — yields chunks as model generates them."""
    stream = ollama.chat(
        model="mistral",
        messages=_build_messages(user_query, inventory_text),
        stream=True
    )
    for chunk in stream:
        content = chunk["message"]["content"]
        if content:
            yield content