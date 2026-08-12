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
    def validate_title(cls, v: Optional[str]) -> Optional[str]:
        """Normalize and validate an optional task title before type coercion.

        Args:
            v (Optional[str]): The raw title value supplied by the
                caller, or None if the field was omitted or explicitly
                set to null.

        Returns:
            Optional[str]: None if ``v`` is None; otherwise the title
            with leading/trailing whitespace stripped.

        Raises:
            ValueError: If the stripped value is empty, or exceeds 200
                characters. Pydantic converts this into a 422 response
                when triggered via a FastAPI request body.

        Confirmed bug (see storage.update_task): this validator does
        not distinguish "field omitted" from "field explicitly set to
        null" — both pass v=None through unchanged. Combined with
        storage.update_task's use of setattr() (which skips Pydantic
        re-validation), an explicit {"title": null} in a PATCH request
        sets the stored title to None and is returned as such with
        HTTP 200, even though TaskResponse.title is a required,
        non-nullable str. Verified by manual testing, not just code
        inspection.
        """
        if v is None:
            return v
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
