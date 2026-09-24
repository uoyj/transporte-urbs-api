"""Modelos SQLAlchemy — reaproveitados do transporte-urbs-ingestor (read-only).

Usamos importlib para carregar *explicitamente* o models.py do ingestor,
evitando conflito de nome com este src/models.py quando /app/src esta no path.
"""
import importlib.util
from pathlib import Path

# Dentro do container: volume monta ingestor src em /shared/ingestor/src (read-only)
# Em desenvolvimento: path relativo ao projeto-ingestor ao lado
_INGESTOR_SRC = Path("/shared/ingestor/src")
if not _INGESTOR_SRC.exists():
    _INGESTOR_SRC = Path(__file__).resolve().parent.parent.parent.parent / \
        "transporte-urbs-ingestor/src"

_spec = importlib.util.spec_from_file_location(
    "urbs_ingestor_models",
    _INGESTOR_SRC / "models.py",
)
_models = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_models)

Base = _models.Base
Linha = _models.Linha
Ponto = _models.Ponto
Horario = _models.Horario
Trajeto = _models.Trajeto

__all__ = ["Base", "Linha", "Ponto", "Horario", "Trajeto"]
