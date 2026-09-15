"""Database session e engine SQLAlchemy (modo somente-leitura)."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool
import os
from dotenv import load_dotenv
from src.models import Base

load_dotenv()

_USER = os.getenv("POSTGRES_USER", "urbs_api_reader")
_PASS = os.getenv("POSTGRES_PASSWORD", "")
_HOST = os.getenv("POSTGRES_HOST", "192.168.2.114")
_PORT = os.getenv("POSTGRES_PORT", "5432")
_DB   = os.getenv("POSTGRES_DB", "urbs_db")

DATABASE_URL = (
    f"postgresql+psycopg2://{_USER}:{_PASS}@{_HOST}:{_PORT}/{_DB}"
)

engine = create_engine(
    DATABASE_URL,
    poolclass=NullPool,
    echo=False,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db():
    """FastAPI dependency — session de leitura por request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
