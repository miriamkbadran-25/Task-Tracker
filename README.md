# Task Tracker

A learning project (AI-Assisted Coding, Module 4) implementing a REST
API backend (FastAPI) with a single-page frontend, backed by
in-memory storage. Tasks have a title, description, status, priority,
and optional assignee; status changes are restricted to a fixed set
of allowed transitions.

This is a learning-project skeleton: no authentication, no database,
no multi-user support, and no deployment configuration beyond the
included `Dockerfile`. See [Project conventions and current
limitations](#project-conventions-and-current-limitations) below.

## Prerequisites

- Python 3.11 (`[VERIFY]`: `backend/README.md` states 3.12, but
  `Dockerfile` and `.github/workflows/ci.yml` both pin 3.11 — this
  README follows the enforced version)
- pip
- Docker (optional, only needed for the "Run with Docker" section)

## Local setup

Run from the repository root:

```bash
cd backend
python -m venv .venv
```

Activate the virtual environment:

```bash
# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# Windows Command Prompt
.venv\Scripts\activate.bat

# macOS/Linux (bash/zsh)
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

The application does not require a `.env` file for the commands in
this README.

## Run the app locally

From the repository root:

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

- API base URL: `http://127.0.0.1:8000`
- Interactive API docs (Swagger UI): `http://127.0.0.1:8000/docs`
- Frontend (Kanban board, served by the backend): `http://127.0.0.1:8000/`
- Health check: `http://127.0.0.1:8000/health`

## Run tests

From the repository root:

```bash
cd backend
pytest -v
```

This is equivalent to the command CI runs (`python -m pytest -v` in
`.github/workflows/ci.yml`).

## Run with Docker

The `Dockerfile` lives at the repository root and builds the backend
plus frontend into a single image. Build and run from the repository
root:

```bash
docker build -t task-tracker .
docker run --rm -p 8000:8000 task-tracker
```

The container's entrypoint runs
`uvicorn app.main:app --host 0.0.0.0 --port 8000` (no `--reload`,
unlike local dev). Once running, the app is available at the same
URLs listed above (`http://127.0.0.1:8000/`, `/docs`, `/health`).

### Docker safety check

- The runtime image switches to the unprivileged `app` user before
  starting Uvicorn.
- `.dockerignore` excludes `.env` and `.env.*`, so environment files
  and their secrets are not sent in the Docker build context.
- Runtime command: `docker run --rm -p 8000:8000 task-tracker`.

## CI workflow summary

Defined in `.github/workflows/ci.yml`:

- Triggers: every `push` and every `pull_request` (no branch filters)
- Runs on `ubuntu-latest`, working directory `backend/`
- Sets up Python 3.11
- Installs `backend/requirements.txt` (which pins `pytest`)
- Runs `python -m pytest -v`

CI only runs the test suite — there is no linting, type-checking,
Docker build/push, or deployment step defined.

## Documentation checks

The following claims were checked against the repository on August 25,
2026. They are source and test-suite checks; a local server and Docker
container were **not run** during this documentation update because
this workspace has no working Python interpreter or Docker CLI.

- **Test command and CI behavior:** `.github/workflows/ci.yml` sets
  `backend/` as the working directory, installs `requirements.txt`,
  and runs `python -m pytest -v` on Python 3.11.
- **Frontend and task endpoint:** `backend/app/main.py` serves the
  frontend from `GET /` and defines `POST /tasks` with HTTP `201
  Created`; `backend/tests/test_frontend_integration.py` asserts both
  behaviors.
- **Docker startup behavior:** `Dockerfile` uses Python 3.11-slim,
  exposes port 8000, switches to the `app` user, and starts Uvicorn
  with `app.main:app --host 0.0.0.0 --port 8000`.

## Project structure

```
task-tracker/
├── .github/
│   └── workflows/
│       └── ci.yml            # CI: installs deps, runs pytest -v
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI app instance + all route handlers
│   │   ├── models.py         # Pydantic models: TaskCreate, TaskUpdate,
│   │   │                     # TaskResponse, TaskStatus, TaskPriority
│   │   ├── storage.py        # In-memory task store (module-level dict)
│   │   ├── business_rules.py # Status transition validation
│   │   ├── routes.py         # empty, unused
│   │   ├── schemas.py        # empty, unused
│   │   ├── services.py       # empty, unused
│   │   └── validators.py     # empty, unused
│   ├── tests/
│   │   ├── test_frontend_integration.py
│   │   ├── verify_a.py
│   │   └── __init__.py
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md             # older, backend-only setup doc — see note below
├── frontend/
│   └── index.html            # single-file Kanban board UI (HTML/CSS/JS)
├── Dockerfile
├── .dockerignore
├── BEHAVIOR_CONTRACT_MODULE3.md  # manual frontend behavior test checklist
└── README.md                 # this file
```

`[VERIFY]`: `backend/app/routes.py`, `schemas.py`, `services.py`, and
`validators.py` are all empty and not imported anywhere — confirmed
by grep. `main.py` calls `storage.py` and `business_rules.py`
directly; there is currently no separate service layer in use,
despite the empty `services.py` stub suggesting one was planned.

## Project conventions and current limitations

**Conventions**

- All request/response models use Pydantic v2 with `extra="forbid"`
  — unknown fields in a request body are rejected.
- Task `status` values are exactly `ToDo`, `InProgress`, `Done`
  (`app/models.py: TaskStatus`); `priority` values are `Low`,
  `Medium`, `High`.
- Allowed status transitions (`app/business_rules.py:
  VALID_TRANSITIONS`): `ToDo → InProgress`, `InProgress → Done`,
  `Done → InProgress`. Any other transition, including submitting the
  same status a task already has, is rejected by
  `validate_status_transition` with HTTP 422 — **except** that
  `PATCH /tasks/{task_id}` only calls this validator when the
  requested status differs from the task's current status, so
  submitting an unchanged status is accepted with 200 rather than
  hitting that rule.

**Current limitations**

- In-memory storage only — all tasks are lost on process restart;
  there is no database.
- No authentication, authorization, or user accounts.
- No multi-tenancy and no real-time updates (no websockets/polling).
- `GET /tasks` does not support filtering by status or priority via
  query parameters, even though `storage.get_all_tasks()` accepts
  both — the route calls it with no arguments. `[VERIFY]` whether
  this is intentional.
- Not production-ready: the `Dockerfile` builds a runnable image, but
  nothing in this repo deploys it anywhere.
- CI runs tests only; there is no linting or type-checking step.

## Related documents

- `BEHAVIOR_CONTRACT_MODULE3.md` — manual behavior-testing checklist
  for the frontend Kanban board (drag-and-drop, modals, error states).
- [`docs/decisions/0001-documentation-verification-approach.md`](docs/decisions/0001-documentation-verification-approach.md)
  — technical decision note on verifying API documentation against a
  running instance instead of from source reading alone.
- `[VERIFY]`: this file's previous version and `backend/README.md`
  both reference an "ADR-001" architecture decision record that could
  not be located anywhere in this repository — confirm whether it
  exists outside this repo or should be recreated. It is a different
  document from the decision note linked above.
