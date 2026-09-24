"""Rotas da API — somente leitura sobre linhas, pontos, horarios e trajetos."""
import hashlib
import json
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy.orm import Session, joinedload

from src.database import get_db
from src.models import Horario, Linha, Ponto, Trajeto
from src.schemas import LinhaResponse

router = APIRouter()


def _flatten_coords(coords: Any) -> list[list[float]]:
    """Achata coordenadas aninhadas de um GeoJSON (MultiLineString, etc)."""
    pontos: list[list[float]] = []
    for item in coords:
        if isinstance(item, list) and len(item) > 0 and isinstance(item[0], list):
            pontos.extend(_flatten_coords(item))
        else:
            pontos.append(item)
    return pontos


def _bbox_from_geojson(geojson: dict[str, Any]) -> Optional[List[float]]:
    """Calcula bbox [min_lng, min_lat, max_lng, max_lat] a partir do snapshot."""
    geometry = geojson.get("geometry") if geojson else None
    if not geometry:
        return None
    coords = _flatten_coords(geometry.get("coordinates", []))
    if not coords:
        return None
    lons = [p[0] for p in coords]
    lats = [p[1] for p in coords]
    return [min(lons), min(lats), max(lons), max(lats)]


@router.get("/linhas", response_model=List[LinhaResponse])
def listar_linhas(
    com_trajeto: bool = Query(False, description="Inclui bbox do trajeto de cada linha"),
    db: Session = Depends(get_db),
):
    """Lista todas as linhas de onibus da URBS."""
    query = db.query(Linha)
    if com_trajeto:
        query = query.options(joinedload(Linha.trajeto))
    linhas = query.order_by(Linha.codigo).all()

    resultado: list[dict[str, Any]] = []
    for linha in linhas:
        item: dict[str, Any] = {
            "id": linha.id,
            "codigo": linha.codigo,
            "nome": linha.nome,
            "origem": linha.origem,
            "destino": linha.destino,
            "cor": linha.cor,
        }
        if com_trajeto:
            item["bbox"] = _bbox_from_geojson(linha.trajeto.geojson_simplificado) if linha.trajeto else None
        resultado.append(item)

    return resultado


@router.get("/linhas/{codigo}/pontos", response_model=List[dict])
def listar_pontos(codigo: str, db: Session = Depends(get_db)):
    """Lista os pontos de uma linha identificada pelo codigo."""
    linha = db.query(Linha).filter(Linha.codigo == codigo).first()
    if not linha:
        raise HTTPException(404, f"Linha {codigo} nao encontrada")

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


@router.get("/linhas/{codigo}/trajeto")
def obter_trajeto(codigo: str, db: Session = Depends(get_db)):
    """Retorna o snapshot GeoJSON do trajeto da linha (application/geo+json)."""
    trajeto = (
        db.query(Trajeto)
        .join(Linha)
        .filter(Linha.codigo == codigo)
        .first()
    )
    if not trajeto:
        raise HTTPException(404, f"Trajeto para linha {codigo} nao encontrado")

    etag = hashlib.sha256(str(trajeto.atualizado_em).encode("utf-8")).hexdigest()
    content = json.dumps(trajeto.geojson_simplificado)

    return Response(
        content=content,
        media_type="application/geo+json",
        headers={
            "Cache-Control": "public, max-age=3600",
            "ETag": etag,
        },
    )


@router.get("/pontos/{codigo}/horarios", response_model=List[dict])
def horarios_ponto(codigo: str, db: Session = Depends(get_db)):
    """Lista os horarios de um ponto identificado pelo codigo."""
    ponto = db.query(Ponto).filter(Ponto.codigo == codigo).first()
    if not ponto:
        raise HTTPException(404, f"Ponto {codigo} nao encontrado")

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
