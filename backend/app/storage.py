import uuid
from datetime import datetime
from typing import Optional
from app.models import TaskCreate, TaskUpdate, TaskResponse, TaskStatus, TaskPriority


_tasks: dict[str, TaskResponse] = {}


def add_task(payload: TaskCreate) -> TaskResponse:
    """Create and persist a new task.

    Args:
        payload (TaskCreate): Validated task data to store.

    Returns:
        TaskResponse: The stored task, with a newly generated UUID ``id``
        and ``created_at``/``updated_at`` both set to the current local
        time.

    [VERIFY]: created_at/updated_at use datetime.now() (naive, local
    time), not datetime.now(timezone.utc) as used in main.health_check.
    Flagging the inconsistency rather than guessing which is intended.
    """
    task_id = str(uuid.uuid4())
    now = datetime.now()
    task = TaskResponse(
        id=task_id,
        title=payload.title,
        description=payload.description,
        status=payload.status,
        priority=payload.priority,
        assignee=payload.assignee,
        created_at=now,
        updated_at=now,
    )
    _tasks[task_id] = task
    return task


def get_all_tasks(status: Optional[TaskStatus] = None, priority: Optional[TaskPriority] = None) -> list[TaskResponse]:
    """List tasks, optionally filtered by status and/or priority.

    Args:
        status (Optional[TaskStatus]): If provided, only tasks with this
            status are returned.
        priority (Optional[TaskPriority]): If provided, only tasks with
            this priority are returned.

    Returns:
        list[TaskResponse]: Matching tasks, in insertion order.

    [VERIFY]: The GET /tasks route in main.py currently calls this
    function with no arguments, so these filters are not exposed via the
    API today.
    """
    tasks = list(_tasks.values())
    if status is not None:
        tasks = [t for t in tasks if t.status == status]
    if priority is not None:
        tasks = [t for t in tasks if t.priority == priority]
    return tasks


def get_task_by_id(task_id: str) -> Optional[TaskResponse]:
    """Look up a single task by id.

    Args:
        task_id (str): The task's unique identifier.

    Returns:
        Optional[TaskResponse]: The matching task, or None if no task
        with that id exists.
    """
    return _tasks.get(task_id)


def update_task(task_id: str, payload: TaskUpdate) -> Optional[TaskResponse]:
    """Apply a partial update to an existing task.

    Args:
        task_id (str): The task's unique identifier.
        payload (TaskUpdate): Fields to update. Only fields explicitly
            set on payload (per model_dump(exclude_unset=True)) are
            applied; omitted fields are left unchanged.

    Returns:
        Optional[TaskResponse]: The updated task, or None if no task
        with ``task_id`` exists. On success, ``updated_at`` is refreshed
        to the current local time.

    [VERIFY]: TaskUpdate.title accepts an explicit null and would set
    the task's title to None if a caller sent {"title": null}, even
    though TaskResponse.title is typed as a non-optional str. Whether
    that's intended, or should be rejected earlier, wasn't clear from
    the code.
    """
    if task_id not in _tasks:
        return None
    
    task = _tasks[task_id]
    update_data = payload.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(task, field, value)
    
    task.updated_at = datetime.now()
    _tasks[task_id] = task
    
    return task


def delete_task(task_id: str) -> bool:
    """Delete a task by id.

    Args:
        task_id (str): The task's unique identifier.

    Returns:
        bool: True if a task was found and deleted, False if no task
        with ``task_id`` existed.
    """
    if task_id in _tasks:
        del _tasks[task_id]
        return True
    return False


def _reset() -> None:
    _tasks.clear()
