import uuid
from datetime import date, datetime
from typing import Optional
from app.models import TaskCreate, TaskUpdate, TaskResponse, TaskStatus, TaskPriority


_tasks: dict[str, TaskResponse] = {}


def _is_overdue(task: TaskResponse) -> bool:
    return task.due_date is not None and task.due_date < date.today() and task.status != TaskStatus.DONE


def _build_task_response(task: TaskResponse) -> TaskResponse:
    task_data = task.model_dump()
    task_data["overdue"] = _is_overdue(task)
    return TaskResponse(**task_data)


def add_task(payload: TaskCreate) -> TaskResponse:
    task_id = str(uuid.uuid4())
    now = datetime.now()
    task = TaskResponse(
        id=task_id,
        title=payload.title,
        description=payload.description,
        status=payload.status,
        priority=payload.priority,
        assignee=payload.assignee,
        due_date=payload.due_date,
        tags=payload.tags,
        created_at=now,
        updated_at=now,
    )
    _tasks[task_id] = task
    return _build_task_response(task)


def get_all_tasks(
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    overdue: Optional[bool] = None,
    tag: Optional[str] = None,
) -> list[TaskResponse]:
    tasks = [_build_task_response(task) for task in _tasks.values()]
    if status is not None:
        tasks = [t for t in tasks if t.status == status]
    if priority is not None:
        tasks = [t for t in tasks if t.priority == priority]
    if overdue is not None:
        tasks = [t for t in tasks if t.overdue is overdue]
    if tag is not None:
        normalized_tag = tag.strip().casefold()
        tasks = [t for t in tasks if any(existing_tag.casefold() == normalized_tag for existing_tag in t.tags)]
    return tasks


def get_task_by_id(task_id: str) -> Optional[TaskResponse]:
    task = _tasks.get(task_id)
    if task is None:
        return None
    return _build_task_response(task)


def update_task(task_id: str, payload: TaskUpdate) -> Optional[TaskResponse]:
    if task_id not in _tasks:
        return None
    
    task = _tasks[task_id]
    update_data = payload.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(task, field, value)
    
    task.updated_at = datetime.now()
    _tasks[task_id] = task
    
    return _build_task_response(task)


def delete_task(task_id: str) -> bool:
    if task_id in _tasks:
        del _tasks[task_id]
        return True
    return False


def _reset() -> None:
    _tasks.clear()
