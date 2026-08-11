import re
from enum import Enum
from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator


MAX_TAGS_PER_TASK: Optional[int] = None
MAX_TAG_LENGTH: Optional[int] = None


def _to_camel_case_tag(value: str) -> str:
    text = str(value).strip()
    if not text:
        return ""

    spaced = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", text)
    spaced = re.sub(r"[^0-9A-Za-z]+", " ", spaced)
    words = [word for word in spaced.split() if word]
    if not words:
        return ""

    parts: list[str] = []
    for word in words:
        if word.isupper() and len(word) > 1:
            parts.append(word)
        else:
            parts.append(word[:1].upper() + word[1:])
    return "".join(parts)


class TaskStatus(str, Enum):
    TODO = "ToDo"
    IN_PROGRESS = "InProgress"
    DONE = "Done"


class TaskPriority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


def _normalize_tags(value: Optional[list[str]]) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValueError("Tags must be provided as a list of strings")

    normalized_tags: list[str] = []
    for tag in value:
        if not isinstance(tag, str):
            raise ValueError("Tags must be provided as a list of strings")

        cleaned_tag = tag.strip()
        if not cleaned_tag:
            raise ValueError("Tags cannot contain empty values")
        if MAX_TAG_LENGTH is not None and len(cleaned_tag) > MAX_TAG_LENGTH:
            raise ValueError(f"Tag must not exceed {MAX_TAG_LENGTH} characters")

        if any(existing.casefold() == cleaned_tag.casefold() for existing in normalized_tags):
            continue
        normalized_tags.append(cleaned_tag)

    if MAX_TAGS_PER_TASK is not None and len(normalized_tags) > MAX_TAGS_PER_TASK:
        raise ValueError(f"Tasks cannot have more than {MAX_TAGS_PER_TASK} tags")

    return normalized_tags


class TaskCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    title: str
    description: str = ""
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    assignee: Optional[str] = None
    due_date: Optional[date] = None
    tags: list[str] = Field(default_factory=list)
    
    @field_validator("title", mode="before")
    @classmethod
    def validate_title(cls, v: str) -> str:
        if v is None:
            raise ValueError("Title cannot be blank")
        v = str(v).strip()
        if not v:
            raise ValueError("Title cannot be blank")
        if len(v) > 200:
            raise ValueError("Title must not exceed 200 characters")
        return v

    @field_validator("due_date")
    @classmethod
    def validate_due_date(cls, v: Optional[date]) -> Optional[date]:
        if v is None:
            return None
        if v < date.today():
            raise ValueError("Due date must be today or later")
        return v

    @field_validator("tags", mode="before")
    @classmethod
    def validate_tags(cls, v: Optional[list[str]]) -> list[str]:
        return _normalize_tags(v)


class TaskUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assignee: Optional[str] = None
    due_date: Optional[date] = None
    tags: Optional[list[str]] = None
    
    @field_validator("title", mode="before")
    @classmethod
    def validate_title(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        v = str(v).strip()
        if not v:
            raise ValueError("Title cannot be blank")
        if len(v) > 200:
            raise ValueError("Title must not exceed 200 characters")
        return v

    @field_validator("due_date")
    @classmethod
    def validate_due_date(cls, v: Optional[date]) -> Optional[date]:
        if v is None:
            return None
        if v < date.today():
            raise ValueError("Due date must be today or later")
        return v

    @field_validator("tags", mode="before")
    @classmethod
    def validate_tags(cls, v: Optional[list[str]]) -> Optional[list[str]]:
        if v is None:
            return None
        return _normalize_tags(v)


class TaskResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    id: str
    title: str
    description: str
    status: TaskStatus
    priority: TaskPriority
    assignee: Optional[str]
    due_date: Optional[date] = None
    tags: list[str] = Field(default_factory=list)
    overdue: bool = False
    created_at: datetime
    updated_at: datetime
