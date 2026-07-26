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
    """
    Simple liveness check endpoint.

    Returns HTTP 200 with the current UTC timestamp in ISO 8601 format.
    """
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/", include_in_schema=False)
def serve_frontend() -> FileResponse:
    frontend_path = Path(__file__).resolve().parents[1] / ".." / "frontend" / "index.html"
    return FileResponse(frontend_path)


@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED, tags=["tasks"])
def create_task(payload: TaskCreate) -> TaskResponse:
    return storage.add_task(payload)


@app.get("/tasks", response_model=list[TaskResponse], tags=["tasks"])
def list_tasks() -> list[TaskResponse]:
    return storage.get_all_tasks()


@app.get("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def get_task(task_id: UUID) -> TaskResponse:
    task = storage.get_task_by_id(str(task_id))
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
    return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["tasks"])
def delete_task(task_id: UUID) -> None:
    deleted = storage.delete_task(str(task_id))
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")


@app.patch("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def update_task(task_id: UUID, payload: TaskUpdate) -> TaskResponse:
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