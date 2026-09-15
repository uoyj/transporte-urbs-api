"""Schemas Pydantic para serialização de respostas (read-only)."""
from pydantic import BaseModel, ConfigDict
from typing import Optional


class LinhaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    codigo: str
    nome: str
    origem: Optional[str] = None
    destino: Optional[str] = None
    cor: Optional[str] = None
