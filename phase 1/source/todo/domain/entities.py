"""
Task entity definition.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

from todo.domain.value_objects import Priority, TaskStatus


@dataclass
class Task:
    """
    Core domain entity representing a todo task.

    Attributes:
        id: Unique identifier (assigned by repository)
        title: Task title (1-200 characters)
        description: Optional task description (0-2000 characters)
        status: Current task status (pending/completed)
        priority: Task priority (HIGH/MEDIUM/LOW, default: MEDIUM)
        tags: List of tags for categorization (default: empty)
        created_at: Timestamp when task was created
        updated_at: Timestamp when task was last modified
    """
    id: int
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING
    priority: Priority = Priority.MEDIUM
    tags: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def _update_timestamp(self) -> None:
        """Update the updated_at timestamp."""
        self.updated_at = datetime.now(timezone.utc)

    def complete(self) -> None:
        """Mark task as complete."""
        self.status = TaskStatus.COMPLETED
        self._update_timestamp()

    def reopen(self) -> None:
        """Reopen a completed task."""
        self.status = TaskStatus.PENDING
        self._update_timestamp()

    def update_title(self, new_title: str) -> None:
        """Update task title."""
        self.title = new_title
        self._update_timestamp()

    def update_description(self, new_description: Optional[str]) -> None:
        """Update task description."""
        self.description = new_description
        self._update_timestamp()

    def update_priority(self, priority: Priority) -> None:
        """Update task priority."""
        self.priority = priority
        self._update_timestamp()

    def add_tag(self, tag: str) -> None:
        """Add a tag to the task (normalized to lowercase)."""
        normalized = tag.strip().lower()
        if normalized and normalized not in self.tags:
            self.tags.append(normalized)
            self._update_timestamp()

    def remove_tag(self, tag: str) -> bool:
        """Remove a tag from the task. Returns True if tag was removed."""
        normalized = tag.strip().lower()
        if normalized in self.tags:
            self.tags.remove(normalized)
            self._update_timestamp()
            return True
        return False

    def has_tag(self, tag: str) -> bool:
        """Check if task has a specific tag (case-insensitive)."""
        normalized = tag.strip().lower()
        return normalized in self.tags
