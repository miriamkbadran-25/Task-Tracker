# Task Tracker Architecture

## What the app does

Task Tracker is a learning-project REST API with a single-page Kanban frontend. It lets users create, view, update, delete, and move tasks across `ToDo`, `InProgress`, and `Done` states; task data is held only in process memory.

## Data model

**Task** is the only persisted entity: `id` (generated UUID string), `title`, `description`, `status`, `priority`, optional `assignee`, `created_at`, and `updated_at`. Titles are required, trimmed, non-blank, and limited to 200 characters. Statuses are `ToDo`, `InProgress`, and `Done`; priorities are `Low`, `Medium`, and `High`. New tasks default to empty description, `ToDo`, `Medium`, and no assignee.

## Request flow: create a task

1. The user submits the New Task form in the Kanban UI.
2. The frontend trims the title, builds JSON, and sends `POST http://localhost:8000/tasks`.
3. FastAPI parses the request as `TaskCreate`; Pydantic rejects invalid fields or values.
4. `create_task` calls the storage layer, which generates a UUID, sets both timestamps, and places the task in the module-level dictionary.
5. The API returns `201 Created` with `TaskResponse`; the frontend reloads the task list and re-renders the board.

## Key files

- `backend/app/main.py` — FastAPI setup, frontend serving, health check, and task CRUD routes.
- `backend/app/models.py` — Pydantic request/response models, enums, defaults, and field validation.
- `backend/app/storage.py` — Module-level in-memory dictionary and task CRUD operations.
- `backend/app/business_rules.py` — Allowed status-transition validation.
- `frontend/index.html` — Complete Kanban UI, including forms, API requests, rendering, and drag-and-drop.
- `backend/requirements.txt` — Pinned FastAPI, Uvicorn, Pydantic, and test dependencies.
- `Dockerfile` — Multi-stage Python 3.11 container build and Uvicorn startup configuration.
- `README.md` — Setup, run, test, CI, and documented-project limitation guidance.

## Conventions

- **Validation:** Pydantic v2 models forbid unknown request fields. Updates apply only supplied fields; explicit `null` is rejected for title, description, status, and priority, while assignee may be null.
- **Storage:** A module-level Python dictionary stores `TaskResponse` objects. Data is lost when the process restarts; timestamps use local naive `datetime.now()`.
- **Error handling:** FastAPI/Pydantic validation failures return HTTP 422; missing task IDs return HTTP 404. Status changes permit only `ToDo → InProgress`, `InProgress → Done`, and `Done → InProgress`.
- **Frontend/backend interaction:** The backend serves the frontend at `/`; the frontend calls the task API with browser `fetch`, maintains a local task array, and refreshes the board after successful form submissions. CORS is configured to allow all origins, methods, headers, and credentials.

## Not visible or assumptions

- Database persistence, authentication/authorization, multi-user behavior, real-time synchronization, deployment beyond Docker, and API filtering through `GET /tasks` are not implemented or not exposed by the visible route.
- Browser behavior and API behavior were inspected from source, not exercised during this task.
- The frontend hard-codes `http://localhost:8000`; whether this is suitable for every deployment environment is not confirmed.
