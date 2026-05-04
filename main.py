from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from models import QueryRequest, QueryResponse
from data_loader import get_data_as_text, get_summary_stats
from ai import ask, ask_stream

app = FastAPI(title="Inventory AI", version="0.3.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

@app.post("/ask", response_model=QueryResponse)
def ask_inventory(req: QueryRequest):
    """Non-streaming JSON response."""
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question empty.")
    inventory = get_data_as_text()
    result = ask(req.question, inventory)
    return QueryResponse(**result)

@app.post("/ask/stream")
def ask_inventory_stream(req: QueryRequest):
    """Streaming plain-text response — frontend accumulates + parses JSON when done."""
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question empty.")
    inventory = get_data_as_text()

    return StreamingResponse(
        ask_stream(req.question, inventory),
        media_type="text/plain; charset=utf-8",
        headers={"X-Accel-Buffering": "no"}   # disables nginx buffering if deployed
    )

@app.get("/stats")
def stats():
    return get_summary_stats()

@app.get("/health")
def health():
    return {"status": "ok", "model": "mistral", "data_source": "csv/excel"}