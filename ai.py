import ollama
import json
import re

SYSTEM_PROMPT = """
You are an intelligent inventory assistant.
You have real inventory data. Think carefully before answering.
Always respond ONLY in valid JSON — no text outside it:
{
  "answer": "human-friendly conversational response",
  "data": [],
  "insight": "useful observation or recommendation",
  "confidence": "high | medium | low"
}
Be specific with numbers. Use ₹ for prices. Sound like a smart human analyst.
"""

def ask(user_query: str, inventory_text: str) -> dict:
    prompt = f"""
INVENTORY DATA:
{inventory_text}

USER QUESTION: {user_query}

Respond ONLY in JSON.
"""
    response = ollama.chat(
        model="mistral",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": prompt}
        ]
    )

    raw = response["message"]["content"]
    raw = re.sub(r"```json|```", "", raw).strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {
            "answer": raw,
            "data": [],
            "insight": "Model response wasn't clean JSON.",
            "confidence": "low"
        }