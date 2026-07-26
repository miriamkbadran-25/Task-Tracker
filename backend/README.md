# Task Tracker API — Backend

A minimal FastAPI backend for the Task Tracker learning project. This
skeleton currently exposes only a health check endpoint; CRUD
functionality for tasks will be added in a later step.

## Tech Stack

- Python 3.12
- FastAPI
- Uvicorn (ASGI server)
- Pydantic
- python-dotenv

## Project Structure
backend/
├── app/
│ ├── init.py
│ ├── main.py # FastAPI app instance and health endpoint
│ ├── routes.py # (empty — API routes, added later)
│ ├── schemas.py # (empty — Pydantic request/response models, added later)
│ ├── models.py # (empty — internal data models, added later)
│ ├── services.py # (empty — business logic, added later)
│ ├── storage.py # (empty — in-memory data store, added later)
│ └── validators.py # (empty — status transition rules, added later)
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
## Setup

1. Create and activate a virtual environment (see commands below).
2. Install dependencies:
```bash
   pip install -r requirements.txt
```
3. Copy `.env.example` to `.env` and adjust values if needed:
```bash
   cp .env.example .env
```

## Running the Server

```bash
uvicorn app.main:app --reload --port 8000
```

The server will be available at `http://127.0.0.1:8000`.

## Testing the Health Endpoint

```bash
curl http://127.0.0.1:8000/health
```

Expected response:

```json
{
  "status": "ok",
  "timestamp": "2026-07-25T12:00:00.000000+00:00"
}
```

## API Documentation (Swagger UI)

Once the server is running, open your browser to:
http://127.0.0.1:8000/docs

## Scope Notes

This skeleton intentionally does **not** include CRUD endpoints,
authentication, a database, Docker configuration, or a frontend. See
the project ADR for the full architecture decision and future
migration path.# Task-Tracker
