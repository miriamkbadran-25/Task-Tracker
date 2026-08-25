# Task Tracker — Architecture (Strategy C)

## What the app does

Task Tracker is a FastAPI REST API that creates, lists, retrieves, updates, and deletes tasks. It also serves a frontend HTML file at `/` and exposes a `/health` liveness endpoint.

## Data model

The primary entity is `Task`.

| Field | Type / rules |
|---|---|
| `id` | Generated UUID string |
| `title` | Required, trimmed, non-blank, maximum 200 characters |
| `description` | String; defaults to `""` on creation |
| `status` | `ToDo`, `InProgress`, or `Done`; defaults to `ToDo` |
| `priority` | `Low`, `Medium`, or `High`; defaults to `Medium` |
| `assignee` | Nullable string; defaults to `null` |
| `created_at` / `updated_at` | Datetime values set by storage |

`TaskCreate` accepts creation fields; `TaskUpdate` supports partial updates; `TaskResponse` is the returned stored-task shape.

## Request flow — create a task

1. A client sends `POST /tasks` with a `TaskCreate` body.
2. The request model rejects unknown fields and validates the title; invalid input is rejected before the handler runs.
3. `create_task` calls `storage.add_task`.
4. Storage generates a UUID, assigns local `datetime.now()` timestamps, builds a `TaskResponse`, and stores it in the module-level `_tasks` dictionary.
5. The API returns the new task with HTTP 201.

## Key files

- `backend/app/main.py` — FastAPI app, routes, CORS configuration, frontend delivery, and API error translation.
- `backend/app/models.py` — Task enums and request/response validation models.
- `backend/app/storage.py` — In-memory task storage and CRUD operations.
- `backend/app/business_rules.py` — Imported for status-transition validation; implementation not visible from the files I read.
- `frontend/index.html` — Served by `/`; frontend implementation not visible from the files I read.

## Conventions

- Validation: Pydantic models forbid unknown request fields. Titles are normalized by trimming; explicit `null` is rejected for update `title`, `description`, `status`, and `priority`. `assignee` remains nullable.
- Storage: Tasks are held in an in-memory module-level dictionary keyed by UUID strings. Persistence beyond the running process is not visible from the files I read.
- Error handling: Missing tasks become HTTP 404 responses in route handlers. Invalid request bodies and invalid UUID path values are handled before or outside handler bodies; their precise response format is not visible from the files I read.
- Frontend/backend interaction: The backend serves `frontend/index.html` at `/` and allows all CORS origins, methods, and headers. The frontend’s API behavior is not visible from the files I read.

## Not visible or assumptions

- Status-transition rules are not visible from the files I read.
- Frontend UI, request behavior, and error presentation are not visible from the files I read.
- Authentication, authorization, database use, deployment, tests, dependency versions, and runtime configuration are not visible from the files I read.
- Whether the frontend file exists and the behavior if it is missing are not visible from the files I read.
