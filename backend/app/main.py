from datetime import datetime, timezone
from pathlib import Path
from uuid import UUID

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from app import storage
from app.business_rules import validate_status_transition
from app.models import TaskCreate, TaskResponse, TaskUpdate

app = FastAPI(
    title="Task Tracker API",
    description="A minimal learning-project REST API for tracking tasks.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check() -> dict:
    """Report service liveness.

    Route:
        GET /health

    Returns:
        dict: A JSON-serializable mapping with:
            - status (str): Always ``"ok"``.
            - timestamp (str): Current UTC time in ISO 8601 format.

    Example:
        GET /health -> {"status": "ok", "timestamp": "2026-08-12T18:03:11.123456+00:00"}
    """
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/", include_in_schema=False)
def serve_frontend() -> FileResponse:
    """Serve the Task Tracker frontend's index.html.

    Route:
        GET / (excluded from the OpenAPI schema)

    Returns:
        FileResponse: The contents of frontend/index.html located at the
        repository root (two levels above app/main.py).

    Raises:
        [VERIFY]: Behavior when frontend/index.html is missing was not
        verified against Starlette's FileResponse implementation and is
        not covered by tests in this repo.
    """
    frontend_path = Path(__file__).resolve().parents[1] / ".." / "frontend" / "index.html"
    return FileResponse(frontend_path)


@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED, tags=["tasks"])
def create_task(payload: TaskCreate) -> TaskResponse:
    """Create a new task.

    Route:
        POST /tasks

    Args:
        payload (TaskCreate): New task data. ``title`` is required
            (non-blank after stripping, max 200 characters);
            ``description``, ``status``, ``priority``, and ``assignee``
            are optional and fall back to their model defaults.

    Returns:
        TaskResponse: The newly created task, including its generated
        ``id``, ``created_at``, and ``updated_at`` timestamps.

    Raises:
        [VERIFY]: This function does not raise directly. Invalid
        payloads (e.g. blank title, title over 200 characters, unknown
        fields) are rejected by FastAPI/Pydantic before this function
        runs, resulting in an HTTP 422 response.

    Example:
        POST /tasks {"title": "Write docs"} -> 201 Created
    """
    return storage.add_task(payload)


@app.get("/tasks", response_model=list[TaskResponse], tags=["tasks"])
def list_tasks() -> list[TaskResponse]:
    """List all tasks.

    Route:
        GET /tasks

    Returns:
        list[TaskResponse]: Every task currently in storage, in no
        guaranteed order.

    [VERIFY]: This route calls storage.get_all_tasks() with no
    arguments, so it does not expose the status/priority filtering that
    the storage layer supports. Flagging in case filtering was intended
    here.

    Example:
        GET /tasks -> 200 OK with a JSON array of tasks.
    """
    return storage.get_all_tasks()


@app.get("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def get_task(task_id: UUID) -> TaskResponse:
    """Retrieve a single task by id.

    Route:
        GET /tasks/{task_id}

    Args:
        task_id (UUID): The task's unique identifier.

    Returns:
        TaskResponse: The matching task.

    Raises:
        HTTPException: 404 if no task with ``task_id`` exists.

    Example:
        GET /tasks/3fa85f64-5717-4562-b3fc-2c963f66afa6 -> 200 OK
    """
    task = storage.get_task_by_id(str(task_id))
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
    return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["tasks"])
def delete_task(task_id: UUID) -> None:
    """Delete a task by id.

    Route:
        DELETE /tasks/{task_id}

    Args:
        task_id (UUID): The task's unique identifier.

    Returns:
        None: Responds with HTTP 204 No Content on success.

    Raises:
        HTTPException: 404 if no task with ``task_id`` exists.

    Example:
        DELETE /tasks/3fa85f64-5717-4562-b3fc-2c963f66afa6 -> 204 No Content
    """
    deleted = storage.delete_task(str(task_id))
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")


@app.patch("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def update_task(task_id: UUID, payload: TaskUpdate) -> TaskResponse:
    """Partially update a task.

    Route:
        PATCH /tasks/{task_id}

    Args:
        task_id (UUID): The task's unique identifier.
        payload (TaskUpdate): Fields to update. Only fields explicitly
            set in the request body are applied (unset fields are left
            unchanged). If ``status`` is provided and differs from the
            task's current status, the transition is validated via
            validate_status_transition; setting ``status`` to its
            current value skips transition validation.

    Returns:
        TaskResponse: The updated task.

    Raises:
        HTTPException: 404 if no task with ``task_id`` exists.
        HTTPException: 422 if ``status`` is provided, differs from the
            current status, and the transition is not allowed (see
            business_rules.validate_status_transition).

    Example:
        PATCH /tasks/{task_id} {"priority": "High"} -> 200 OK
    """
    # If a new status is provided, validate the transition only when it changes
    if payload.status is not None:
        existing = storage.get_task_by_id(str(task_id))
        if existing is None:
            raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
        if payload.status != existing.status:
            validate_status_transition(existing.status, payload.status)

    task = storage.update_task(str(task_id), payload)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
    return task