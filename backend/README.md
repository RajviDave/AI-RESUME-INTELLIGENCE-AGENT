# AI Resume Intelligence Agent Backend

Production-ready FastAPI starter for resume upload, authentication, PostgreSQL persistence, Alembic migrations, middleware, and modular API routing.

## Quick Start

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
copy .env.example .env
alembic upgrade head
uvicorn app.main:app --reload
```

Health check:

```text
GET http://localhost:8000/api/v1/health
```

Docker:

```bash
copy .env.example .env
docker compose up --build
```

## Environment

Configure runtime values in `.env`. The app uses `pydantic-settings`.

## Migrations

```bash
alembic revision --autogenerate -m "message"
alembic upgrade head
```
