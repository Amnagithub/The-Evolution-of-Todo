"""
Task service for business logic.
"""

from typing import Optional

from todo.domain.entities import Task
from todo.domain.errors import TaskNotFoundError, ValidationError
from todo.domain.repository import TaskRepository
from todo.domain.value_objects import TaskStatus


class TaskService:
    """Service for task operations."""

    def __init__(self, repository: TaskRepository):
        self._repo = repository

    def create_task(
        self,
        title: str,
        description: Optional[str] = None
    ) -> Task:
        """Create a new task."""
        # Validate title
        title = title.strip()
        if not title:
            raise ValidationError("Title cannot be empty")
        if len(title) > 500:
            raise ValidationError("Title exceeds maximum length of 500 characters")

        # Validate description
        if description is not None and len(description) > 2000:
            raise ValidationError("Description exceeds maximum length of 2000 characters")

        # Create task
        task_id = self._repo.get_next_id()
        task = Task(
            id=task_id,
            title=title,
            description=description.strip() if description else None
        )
        return self._repo.save(task)

    def get_task(self, task_id: int) -> Task:
        """Get a task by ID."""
        task = self._repo.get_by_id(task_id)
        if task is None:
            raise TaskNotFoundError(task_id)
        return task

    def get_all_tasks(self) -> list[Task]:
        """Get all tasks sorted by ID."""
        return sorted(self._repo.get_all(), key=lambda t: t.id)

    def mark_task_complete(self, task_id: int) -> Task:
        """Mark a task as complete."""
        task = self.get_task(task_id)
        task.complete()
        return self._repo.save(task)

    def mark_task_incomplete(self, task_id: int) -> Task:
        """Reopen a completed task."""
        task = self.get_task(task_id)
        task.reopen()
        return self._repo.save(task)

    def update_task_title(self, task_id: int, new_title: str) -> Task:
        """Update task title."""
        task = self.get_task(task_id)
        new_title = new_title.strip()
        if not new_title:
            raise ValidationError("Title cannot be empty")
        if len(new_title) > 500:
            raise ValidationError("Title exceeds maximum length of 500 characters")
        task.update_title(new_title)
        return self._repo.save(task)

    def update_task_description(
        self,
        task_id: int,
        new_description: Optional[str]
    ) -> Task:
        """Update task description."""
        task = self.get_task(task_id)
        if new_description is not None:
            new_description = new_description.strip()
            if len(new_description) > 2000:
                raise ValidationError(
                    "Description exceeds maximum length of 2000 characters"
                )
        task.update_description(new_description)
        return self._repo.save(task)

    def delete_task(self, task_id: int) -> bool:
        """Delete a task."""
        if not self._repo.exists(task_id):
            raise TaskNotFoundError(task_id)
        return self._repo.delete(task_id)
