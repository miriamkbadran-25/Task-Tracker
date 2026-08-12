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

    @field_validator("description", mode="before")
    @classmethod
    def validate_description(cls, v: Optional[str]) -> str:
        """Reject an explicit null description before type coercion.

        Pydantic only invokes this validator when the ``description``
        key is present in the input; an omitted key skips it entirely
        and keeps the field's default of ``None``, same as title.

        Args:
            v (Optional[str]): The raw description value supplied by
                the caller. Only called when the ``description`` key is
                present in the request body.

        Returns:
            str: ``v`` unchanged. Unlike title, this does not strip
            whitespace or enforce a length limit, since
            TaskCreate.description has no such rules either — it only
            requires a str, defaulting to ``""``. This validator closes
            the null-bypass gap without inventing constraints
            TaskCreate doesn't already have.

        Raises:
            ValueError: If ``v`` is None (i.e. the caller explicitly
                sent ``{"description": null}``). storage.update_task
                applies updates via setattr() without re-validating, so
                an explicit null would otherwise be stored and returned
                as ``"description": null`` even though
                TaskResponse.description is a required, non-nullable
                str (confirmed by manual testing before this fix).
        """
        if v is None:
            raise ValueError("Description cannot be null")
        return v

    @field_validator("priority", mode="before")
    @classmethod
    def validate_priority(cls, v: Optional[TaskPriority]) -> TaskPriority:
        """Reject an explicit null priority before enum coercion.

        Pydantic only invokes this validator when the ``priority`` key
        is present in the input; an omitted key skips it entirely and
        keeps the field's default of ``None``.

        Args:
            v (Optional[TaskPriority]): The raw priority value supplied
                by the caller. Only called when the ``priority`` key is
                present in the request body.

        Returns:
            TaskPriority: ``v`` unchanged, still subject to Pydantic's
            normal enum-membership validation afterward.

        Raises:
            ValueError: If ``v`` is None (i.e. the caller explicitly
                sent ``{"priority": null}``). storage.update_task
                applies updates via setattr() without re-validating, so
                an explicit null would otherwise be stored and returned
                as ``"priority": null`` even though
                TaskResponse.priority is a required, non-nullable enum
                (confirmed by manual testing before this fix).
        """
        if v is None:
            raise ValueError("Priority cannot be null")
        return v

    @field_validator("status", mode="before")
    @classmethod
    def validate_status(cls, v: Optional[TaskStatus]) -> TaskStatus:
        """Reject an explicit null status before enum coercion.

        Pydantic only invokes this validator when the ``status`` key is
        present in the input; an omitted key skips it entirely and
        keeps the field's default of ``None``. This distinction matters
        more here than for the other fields: main.update_task checks
        ``payload.status is not None`` to decide whether a status
        change was requested at all, and only omission should mean
        "leave status unchanged" — an explicit null is a malformed
        request, not a no-op.

        Args:
            v (Optional[TaskStatus]): The raw status value supplied by
                the caller. Only called when the ``status`` key is
                present in the request body.

        Returns:
            TaskStatus: ``v`` unchanged, still subject to Pydantic's
            normal enum-membership validation afterward.

        Raises:
            ValueError: If ``v`` is None (i.e. the caller explicitly
                sent ``{"status": null}``). Before this fix,
                storage.update_task's setattr()-based apply would store
                and return ``"status": null`` (a schema violation,
                since TaskResponse.status is required and non-nullable)
                and, worse, would silently skip
                business_rules.validate_status_transition entirely,
                since main.update_task's ``is not None`` guard treated
                an explicit null the same as "no status provided"
                (confirmed by manual testing before this fix).
        """
        if v is None:
            raise ValueError("Status cannot be null. Omit the field entirely to leave status unchanged.")
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
