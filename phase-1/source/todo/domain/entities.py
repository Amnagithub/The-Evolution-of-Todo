"""
Task entity definition.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

from todo.domain.value_objects import TaskStatus


@dataclass
class Task:
    """
    Core domain entity representing a todo task.

    Attributes:
        id: Unique identifier (assigned by repository)
        title: Task title (1-500 characters)
        description: Optional task description (0-2000 characters)
        status: Current task status (pending/completed)
        created_at: Timestamp when task was created
        completed_at: Timestamp when task was completed (None if pending)
    """
    id: int
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None

    def complete(self) -> None:
        """Mark task as complete."""
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.now(timezone.utc)

    def reopen(self) -> None:
        """Reopen a completed task."""
        self.status = TaskStatus.PENDING
        self.completed_at = None

    def update_title(self, new_title: str) -> None:
        """Update task title."""
        self.title = new_title

    def update_description(self, new_description: Optional[str]) -> None:
        """Update task description."""
        self.description = new_description
