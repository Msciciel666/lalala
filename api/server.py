"""Minimal REST API server using FastAPI."""

from fastapi import FastAPI

app = FastAPI(title="darkweb666 API")


@app.get("/status", summary="Health check", response_model=dict)
async def status() -> dict:
    """Return service status."""
    return {"status": "ok"}
