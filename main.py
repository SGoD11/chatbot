from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import QueryRequest, QueryResponse
from data_loader import get_data_as_text, get_summary_stats
from ai import ask

app = FastAPI(title="Inventory AI", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/ask", response_model=QueryResponse)
def ask_inventory(req: QueryRequest):
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question empty.")
    inventory = get_data_as_text()
    result = ask(req.question, inventory)
    return QueryResponse(**result)

@app.get("/stats")
def stats():
    """Quick inventory summary — no AI needed."""
    return get_summary_stats()

@app.get("/health")
def health():
    return {"status": "ok", "model": "mistral", "data_source": "csv/excel"}