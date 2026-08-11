# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

Run from `backend/`:

```bash
# install deps (pytest is not pinned in requirements.txt, install it too)
pip install -r requirements.txt pytest

# start the server (also serves the frontend at the root route)
uvicorn app.main:app --reload --port 8000

# run the full test suite
pytest -q
# or
python -m pytest -q

# run a single test file / test
pytest tests/test_tasks.py
pytest tests/test_tasks.py::test_create_task_valid_returns_201_with_full_body
```

The API is served at `http://127.0.0.1:8000`; the frontend is served by the same backend process at `http://127.0.0.1:8000/` (see `serve_frontend` in `app/main.py`), so there's no separate frontend dev server or build step.

## Architecture

- `backend/app/main.py` — FastAPI app, CORS middleware, and all route handlers. Read this first for the API surface.
- `backend/app/models.py` — Pydantic v2 schemas (`TaskCreate`, `TaskUpdate`, `TaskResponse`), the `TaskStatus`/`TaskPriority` enums, and tag normalization (trim, case-insensitive de-dupe preserving first-seen casing).
- `backend/app/storage.py` — in-memory storage (module-level `_tasks` dict, no database). Also computes `overdue` on read (`due_date < today` and `status != Done`) rather than storing it.
- `backend/app/business_rules.py` — **status transition rules live here**, not in `main.py` or `models.py`. `main.py` only calls `validate_status_transition(existing, new)`.
- `backend/app/routes.py`, `schemas.py`, `services.py`, `validators.py` — present in the tree but currently empty/unused. Don't assume logic lives there.
- `backend/tests/` — pytest suite (`test_tasks.py`, `test_tags.py`, `test_due_dates.py`, `test_frontend_integration.py`). `conftest.py` provides a `client` fixture (`TestClient(app)`) and an autouse fixture that resets `storage._tasks` between tests via `storage._reset()`.
- `frontend/index.html` — single-file vanilla HTML/CSS/JS Kanban UI (no framework, no build step), fetched against the backend API. Implements explicit board states (`loading`, `ready`, `empty`, `error`) and inline field-level validation errors in the task modal.
- `docs/` — verification notes and project docs.
- `BEHAVIOR_CONTRACT_MODULE3.md` — manual QA behavior contract for the frontend Kanban board (columns, drag-and-drop, modals, error states) — useful as a reference when changing frontend behavior.

### Task status model

Status values (`TaskStatus` in `models.py`): `ToDo`, `InProgress`, `Done`. New tasks default to `ToDo`.

Allowed transitions (`business_rules.py::VALID_TRANSITIONS`, enforced only in `PATCH /tasks/{id}` when `status` is included in the payload):
- `ToDo → InProgress`
- `InProgress → Done`
- `Done → InProgress`

Any other transition — including same-status patches (e.g. `ToDo → ToDo`) and skips (e.g. `ToDo → Done`, `Done → ToDo`) — is rejected with `422`.

### API surface (`app/main.py`)

- `GET /health` — liveness check
- `GET /` — serves `frontend/index.html` (excluded from OpenAPI schema)
- `POST /tasks` — 201 on success
- `GET /tasks` — filterable by `status`, `priority`, `overdue`, `tag`
- `GET /tags/suggestions?q=` — reads tags directly off `storage._tasks`
- `GET /tasks/{task_id}` — 404 if missing
- `PATCH /tasks/{task_id}` — 404 if missing, 422 on invalid status transition
- `DELETE /tasks/{task_id}` — 204 on success, 404 if missing

CORS (`main.py`) is currently wide open: `allow_origins=["*"]` combined with `allow_credentials=True`, plus `allow_methods=["*"]` and `allow_headers=["*"]`.

## Constraints

- Storage is intentionally in-memory only — do not add a database or persistence layer.
- Do not add authentication/authorization.
- Do not add deployment steps or infrastructure config.
- Do not make major UI changes to `frontend/index.html`.

Ask first if a task seems to require any of the above.
