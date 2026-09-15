"""FastAPI application — API somente-leitura transporte URBS."""
from fastapi import FastAPI

from src.router import router

app = FastAPI(
    title="Transporte URBS API",
    description="API somente-leitura para linhas, pontos e horários da URBS (Curitiba).",
    version="0.1.0",
)

app.include_router(router)


@app.get("/health")
def health():
    return {"status": "ok"}
