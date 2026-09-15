# transporte-urbs-api

API somente-leitura para dados da URBS (Curitiba), construída com FastAPI + SQLAlchemy.

## Endpoints

| Método | Rota                              | Descrição                              |
|--------|-----------------------------------|----------------------------------------|
| GET    | `/linhas`                         | Lista todas as linhas de ônibus        |
| GET    | `/linhas/{codigo}/pontos`         | Lista pontos de uma linha              |
| GET    | `/pontos/{codigo}/horarios`       | Lista horários de um ponto             |
| GET    | `/health`                         | Healthcheck                            |
| GET    | `/docs`                           | Documentação automática Swagger UI     |

## Stack

- FastAPI + Uvicorn
- SQLAlchemy 2.0 (read-only queries)
- Psycopg2 para PostgreSQL
- Python 3.13-slim

## Deploy (LXC 115)

```bash
docker compose build
docker compose up -d
```

A API roda na porta `8000` e se conecta ao Postgres em `192.168.2.114:5432`
via variáveis de ambiente no `.env`.

## Modelos

Os models (`Linha`, `Ponto`, `Horario`) são importados diretamente do
`transporte-urbs-ingestor` para evitar duplicação de lógica. Esta API é
exclusivamente leitura.
