# Task Tracker API — Backend

A FastAPI backend for the Task Tracker learning project. It serves the
single-page frontend and provides task creation, listing, retrieval,
update, and deletion endpoints in addition to the health check.

## Tech Stack

- Python 3.11 (pinned by the repository Dockerfile and CI workflow)
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

## Running automated tests

From the `backend/` directory, after installing dependencies:

```bash
python -m pytest -v
```

Verified in this workspace on August 25, 2026 with Python 3.11.9:
`backend/.venv` passed `python -m pip check`, and all 3 tests passed.

## Docker

Build and run the full application from the repository root:

```bash
docker build -t task-tracker .
docker run --rm -p 8000:8000 task-tracker
```

`compose.yaml` provides the equivalent Compose setup, including a
health check:

```bash
docker compose up --build
```

Verified in this workspace on August 25, 2026 with Docker Desktop
4.88.1 / Docker Engine 29.7.2: Compose rebuilt the image, its health
check reached `healthy`, and `GET /health` returned `{"status": "ok", ...}`.

## Scope Notes

The project intentionally does **not** include authentication, a
database, or multi-user support. It includes Docker configuration and
a frontend at the repository root; see the root `README.md` for the
full setup and runtime guidance.
