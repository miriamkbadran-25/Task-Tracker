from fastapi import HTTPException, status
from app.models import TaskStatus

VALID_TRANSITIONS: frozenset[tuple[TaskStatus, TaskStatus]] = frozenset({
    (TaskStatus.TODO, TaskStatus.IN_PROGRESS),
    (TaskStatus.IN_PROGRESS, TaskStatus.DONE),
    (TaskStatus.DONE, TaskStatus.IN_PROGRESS),
})


def validate_status_transition(current: TaskStatus, new: TaskStatus) -> None:
    """Validate that a task status change is allowed.

    Args:
        current (TaskStatus): The task's existing status.
        new (TaskStatus): The status being transitioned to.

    Returns:
        None: Returns nothing when the transition is allowed.

    Raises:
        HTTPException: 422 if (current, new) is not one of the allowed
            transitions in VALID_TRANSITIONS (ToDo->InProgress,
            InProgress->Done, Done->InProgress). This includes any
            same-status "transition" (e.g. ToDo->ToDo), which is never
            in VALID_TRANSITIONS.

    [VERIFY]: In app/main.py, update_task only calls this function when
    the new status differs from the current one, so the same-status-is-
    invalid branch described above is not currently reachable through
    the API. Flagging in case that guard is meant to apply here too.
    """
    # Same -> same is invalid. Anything not in VALID_TRANSITIONS is invalid.
    if (current, new) not in VALID_TRANSITIONS:
        allowed = sorted({f"{f.value}->{t.value}" for f, t in VALID_TRANSITIONS})
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid status transition from {current.value} to {new.value}. Allowed transitions: {allowed}",
        )
