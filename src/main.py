"""FastAPI application — API somente-leitura transporte URBS."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.router import router

app = FastAPI(
    title="Transporte URBS API",
    description="API somente-leitura para linhas, pontos e horários da URBS (Curitiba).",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8081", "http://192.168.2.115:8081"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/health")
def health():
    return {"status": "ok"}
