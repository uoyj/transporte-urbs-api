"""FastAPI application — API somente-leitura transporte URBS."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.router import router

import os

app = FastAPI(
    title="Transporte URBS API",
    description="API somente-leitura para linhas, pontos e horários da URBS (Curitiba).",
    version="0.1.0",
)


app = FastAPI(title="Transporte URBS API")

# CORS origins vêm do .env (não-commitado); fallback seguro para dev local
cors_origins = [
    o.strip() for o in os.getenv("CORS_ORIGINS", "http://localhost:8081").split(",")
    if o.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/health")
def health():
    return {"status": "ok"}
