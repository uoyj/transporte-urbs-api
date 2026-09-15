"""Rotas da API — somente leitura sobre linhas, pontos e horários."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.database import get_db
from src.models import Linha, Ponto, Horario
from src.schemas import LinhaResponse

router = APIRouter()


@router.get("/linhas", response_model=List[LinhaResponse])
def listar_linhas(db: Session = Depends(get_db)):
    """Lista todas as linhas de ônibus da URBS."""
    return db.query(Linha).order_by(Linha.codigo).all()


@router.get("/linhas/{codigo}/pontos", response_model=List[dict])
def listar_pontos(codigo: str, db: Session = Depends(get_db)):
    """Lista os pontos de uma linha identificada pelo código."""
    linha = db.query(Linha).filter(Linha.codigo == codigo).first()
    if not linha:
        raise HTTPException(404, f"Linha {codigo} não encontrada")

    pontos = (
        db.query(Ponto)
        .filter(Ponto.linha_id == linha.id)
        .order_by(Ponto.codigo)
        .all()
    )
    return [
        {
            "id": p.id,
            "codigo": p.codigo,
            "latitude": float(p.latitude) if p.latitude else None,
            "longitude": float(p.longitude) if p.longitude else None,
            "descricao": p.descricao,
        }
        for p in pontos
    ]


@router.get("/pontos/{codigo}/horarios", response_model=List[dict])
def horarios_ponto(codigo: str, db: Session = Depends(get_db)):
    """Lista os horários de um ponto identificado pelo código."""
    ponto = db.query(Ponto).filter(Ponto.codigo == codigo).first()
    if not ponto:
        raise HTTPException(404, f"Ponto {codigo} não encontrado")

    horarios = (
        db.query(Horario)
        .filter(Horario.ponto_id == ponto.id)
        .order_by(Horario.dia_semana, Horario.hora)
        .all()
    )
    return [
        {
            "id": h.id,
            "ponto_id": h.ponto_id,
            "dia_semana": h.dia_semana,
            "hora": h.hora,
        }
        for h in horarios
    ]
