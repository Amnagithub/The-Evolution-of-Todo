"""Task model and schemas for SQLModel."""
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, String


class Task(SQLModel, table=True):
    """Task database model."""
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(min_length=1, max_length=200, nullable=False)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    user_id: str = Field(sa_column=Column(String(255), index=True, nullable=False))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TaskCreate(SQLModel):
    """Schema for creating a new task."""
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = None


class TaskUpdate(SQLModel):
    """Schema for updating an existing task (partial)."""
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = None


class TaskToggle(SQLModel):
    """Schema for toggling task completion."""
    completed: bool


class TaskResponse(SQLModel):
    """Schema for task response (excludes user_id)."""
    id: int
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime
