from enum import Enum
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_validator


class TaskStatus(str, Enum):
    TODO = "ToDo"
    IN_PROGRESS = "InProgress"
    DONE = "Done"


class TaskPriority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class TaskCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    title: str
    description: str = ""
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    assignee: Optional[str] = None
    
    @field_validator("title", mode="before")
    @classmethod
    def validate_title(cls, v: str) -> str:
        """Normalize and validate a task title before type coercion.

        Args:
            v (str): The raw title value supplied by the caller.

        Returns:
            str: The title with leading/trailing whitespace stripped.

        Raises:
            ValueError: If ``v`` is None, or the stripped value is
                empty, or it exceeds 200 characters. Pydantic converts
                this into a 422 response when triggered via a FastAPI
                request body.
        """
        if v is None:
            raise ValueError("Title cannot be blank")
        v = str(v).strip()
        if not v:
            raise ValueError("Title cannot be blank")
        if len(v) > 200:
            raise ValueError("Title must not exceed 200 characters")
        return v


class TaskUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assignee: Optional[str] = None
    
    @field_validator("title", mode="before")
    @classmethod
    def validate_title(cls, v: Optional[str]) -> str:
        """Normalize and validate an optional task title before type coercion.

        Pydantic only invokes a field's validator when that field's key
        is present in the input (including an explicit ``null``); a
        wholly omitted ``title`` key skips this validator and keeps the
        field's default of ``None``, without setattr in
        storage.update_task ever touching it. This was verified by
        manual testing: with this fix in place, ``PATCH`` with no
        ``title`` key still returns 200 and leaves the stored title
        unchanged, while ``PATCH {"title": null}`` is rejected below.

        Args:
            v (Optional[str]): The raw title value supplied by the
                caller. Only called when the ``title`` key is present in
                the request body.

        Returns:
            str: The title with leading/trailing whitespace stripped.
            Never returns None.

        Raises:
            ValueError: If ``v`` is None (i.e. the caller explicitly
                sent ``{"title": null}``), or the stripped value is
                empty, or it exceeds 200 characters. Pydantic converts
                this into a 422 response when triggered via a FastAPI
                request body. This mirrors TaskCreate.validate_title,
                which already rejects None the same way — previously
                TaskUpdate was inconsistent with TaskCreate here, which
                let an explicit null title bypass validation and get
                stored (see storage.update_task's history for the
                confirmed bug this fixes).
        """
        if v is None:
            raise ValueError("Title cannot be blank")
        v = str(v).strip()
        if not v:
            raise ValueError("Title cannot be blank")
        if len(v) > 200:
            raise ValueError("Title must not exceed 200 characters")
        return v


class TaskResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    id: str
    title: str
    description: str
    status: TaskStatus
    priority: TaskPriority
    assignee: Optional[str]
    created_at: datetime
    updated_at: datetime
