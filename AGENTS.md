# AGENTS.md — Module 5 Task Tracker

## Project summary

Task Tracker is a learning-project REST API with a single-page Kanban frontend. The backend manages tasks in an in-memory store; the frontend is served at `/` by the FastAPI app. The project has no authentication, database, multi-user support, or deployment configuration beyond the included Dockerfile.

Sources: `README.md`, `backend/app/main.py`, `backend/app/storage.py`, and `frontend/index.html`.

## Tech stack

- Python 3.11 is confirmed by `README.md` and `Dockerfile`. `backend/README.md` says Python 3.12; treat that as outdated or verify before changing the runtime.
- FastAPI, Uvicorn, Pydantic v2, pytest, and httpx are pinned in `backend/requirements.txt`.
- Frontend: a single HTML/CSS/JavaScript file at `frontend/index.html`.
- Persistence: module-level in-memory Python dictionary in `backend/app/storage.py`. Task data is lost when the process restarts.
- Docker is supported by the root `Dockerfile`.

## Supported commands

Run commands from the repository root unless noted otherwise.

```bash
cd backend
python -m venv venv
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Run the automated tests:

```bash
cd backend
pytest -v
```

Build and run the container:

```bash
docker build -t task-tracker .
docker run --rm -p 8000:8000 task-tracker
```

The backend is available at `http://127.0.0.1:8000`; confirmed endpoints include `/`, `/health`, `/docs`, and `/tasks`. Linting, formatting, type-checking, and deployment commands are not confirmed.

Sources: `README.md`, `Dockerfile`, `backend/requirements.txt`, and `backend/app/main.py`.

## Visible business rules

- Statuses are exactly `ToDo`, `InProgress`, and `Done`.
- Priorities are exactly `Low`, `Medium`, and `High`.
- A new task requires a title. Titles are trimmed, cannot be blank, and cannot exceed 200 characters.
- New-task defaults are: `description=""`, `status="ToDo"`, `priority="Medium"`, and `assignee=null`.
- Create and update request models reject unknown fields.
- For updates, omitted fields remain unchanged. Explicit `null` is rejected for `title`, `description`, `status`, and `priority`; `assignee` is nullable.
- Allowed status changes are `ToDo → InProgress`, `InProgress → Done`, and `Done → InProgress`.
- An API PATCH that supplies the task's existing status is accepted because transition validation runs only if the status changes.
- Task IDs are generated UUIDs. Missing tasks return 404 through the API; invalid UUID path values are rejected by FastAPI validation.
- `GET /tasks` lists all tasks. Storage-layer status/priority filters exist but are not exposed by the route.
- Task timestamps use local naive `datetime.now()` in storage; `/health` uses a UTC ISO-8601 timestamp.

Sources: `backend/app/models.py`, `backend/app/business_rules.py`, `backend/app/storage.py`, and `backend/app/main.py`.

## Module 5 working guardrails

- Docs-first: read the relevant repository documentation and implementation before making claims or proposing changes. Mark unverified behavior as **not confirmed**.
- Read-only by default: inspect, analyze, and report without modifying repository files unless the user explicitly authorizes the change.
- One task per thread: keep each Codex task focused on one concrete request. Ask for a new task/thread for unrelated work.
- Do not modify `app/` unless the user explicitly approves an application-code change. This includes `backend/app/` and any other application source directory.
- When documentation describes runtime behavior, prefer verified execution evidence where available; otherwise distinguish code-visible behavior from behavior that is not confirmed.

Source: `docs/decisions/0001-documentation-verification-approach.md`; Module 5-specific requirements are user-provided governance instructions.

## Security and governance

- Never paste, log, commit, or expose secrets, tokens, credentials, private keys, `.env` contents, or other sensitive data.
- Do not run destructive commands or irreversible operations unless explicitly authorized and the target is confirmed.
- Cite the files and relevant code locations that support findings and proposed changes.
- Do not invent findings, test results, requirements, commands, or behavior. State **not confirmed** when the repository evidence is absent or conflicting.
- Do not invent content or findings attributed to the “AI-Assisted Coding - Module 5 Prompt Library”; use only material explicitly provided or present in the repository.
