# Task Tracker Architecture

## What the app does

Task Tracker is a learning-project Kanban application for creating, viewing, updating, moving, and deleting tasks. A FastAPI backend exposes a REST API and serves a single-page HTML/JavaScript frontend; task data lives only in process memory.

## Data model

**Task**: `id` (generated UUID string), `title`, `description`, `status`, `priority`, optional `assignee`, `created_at`, and `updated_at`. Status is one of `ToDo`, `InProgress`, or `Done`; priority is `Low`, `Medium`, or `High`. New tasks default to an empty description, `ToDo`, `Medium`, and no assignee.

## Request flow: create task

1. The browser’s New Task form trims and checks that the title is non-empty, then sends JSON to `POST /tasks`.
2. FastAPI parses the body as `TaskCreate`; Pydantic rejects unknown fields and invalid values.
3. `storage.add_task()` generates a UUID and timestamps, constructs a `TaskResponse`, and saves it in the module-level task dictionary.
4. The API returns `201 Created` with the task. The frontend refreshes its local board data from `GET /tasks` and renders the task in its status column.

## Key files

- `README.md` — current project overview, run instructions, conventions, and limitations.
- `backend/app/main.py` — FastAPI application, frontend serving, and task CRUD routes.
- `backend/app/models.py` — Pydantic request/response schemas and task enums.
- `backend/app/storage.py` — in-memory dictionary and task persistence operations.
- `backend/app/business_rules.py` — allowed task-status transition validation.
- `frontend/index.html` — complete Kanban UI, styling, and browser-side API calls.
- `backend/tests/test_frontend_integration.py` — integration coverage for frontend serving and core task operations.
- `Dockerfile` — Python 3.11 container build and Uvicorn runtime configuration.
- `docs/decisions/0001-documentation-verification-approach.md` — decision note requiring runtime verification for behavior documentation.

## Conventions

- **Validation:** Pydantic v2 models use `extra="forbid"`; titles are trimmed, required, and limited to 200 characters. Explicit `null` is rejected for non-nullable update fields.
- **Storage:** Tasks use a module-level Python dictionary and are lost on restart. UUIDs are generated in storage; task timestamps use local naive `datetime.now()`.
- **Error handling:** FastAPI/Pydantic validation failures return 422; missing tasks return 404; invalid status changes return 422. Allowed changes are `ToDo → InProgress`, `InProgress → Done`, and `Done → InProgress`.
- **Frontend/backend interaction:** The frontend is served at `/`, calls `/tasks` with `fetch`, keeps a browser-side task list, and rerenders the board after changes. It optimistically displays drag-and-drop status moves, reverting them if the PATCH request fails.

## Not visible or assumptions

Runtime behavior was not executed for this document; statements are based on repository source and existing documentation. Authentication, a database, persistence across restarts, multi-user support, deployment automation, and real-time synchronization are not present in the inspected implementation. The intended timezone convention for task timestamps is not confirmed because task storage uses local naive timestamps while `/health` uses UTC.
