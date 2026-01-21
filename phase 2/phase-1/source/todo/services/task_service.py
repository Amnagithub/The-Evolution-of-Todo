"""
Task service for business logic.
"""

from typing import Optional

from todo.domain.entities import Task
from todo.domain.errors import TaskNotFoundError, ValidationError
from todo.domain.repository import TaskRepository
from todo.domain.value_objects import Priority, TaskStatus


class TaskService:
    """Service for task operations."""

    def __init__(self, repository: TaskRepository):
        self._repo = repository

    def create_task(
        self,
        title: str,
        description: Optional[str] = None,
        priority: Priority = Priority.MEDIUM,
        tags: Optional[list[str]] = None
    ) -> Task:
        """Create a new task."""
        # Validate title
        title = title.strip()
        if not title:
            raise ValidationError("Title cannot be empty")
        if len(title) > 200:
            raise ValidationError("Title must be 200 characters or less")

        # Validate description
        if description is not None and len(description) > 2000:
            raise ValidationError("Description must be 2000 characters or less")

        # Validate and normalize tags
        normalized_tags = []
        if tags:
            for tag in tags:
                normalized = tag.strip().lower()
                if not normalized:
                    raise ValidationError("Tag cannot be empty")
                if len(normalized) > 50:
                    raise ValidationError("Tag must be 50 characters or less")
                if normalized in normalized_tags:
                    raise ValidationError(f"Duplicate tag: '{tag}'")
                normalized_tags.append(normalized)

        # Create task
        task_id = self._repo.get_next_id()
        task = Task(
            id=task_id,
            title=title,
            description=description.strip() if description else None,
            priority=priority,
            tags=normalized_tags
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
        if len(new_title) > 200:
            raise ValidationError("Title must be 200 characters or less")
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
                    "Description must be 2000 characters or less"
                )
        task.update_description(new_description)
        return self._repo.save(task)

    def update_task_priority(self, task_id: int, priority: Priority) -> Task:
        """Update task priority."""
        task = self.get_task(task_id)
        task.update_priority(priority)
        return self._repo.save(task)

    def add_task_tag(self, task_id: int, tag: str) -> Task:
        """Add a tag to a task."""
        task = self.get_task(task_id)
        normalized = tag.strip().lower()
        if not normalized:
            raise ValidationError("Tag cannot be empty")
        if len(normalized) > 50:
            raise ValidationError("Tag must be 50 characters or less")
        if normalized in task.tags:
            raise ValidationError(f"Tag '{tag}' already exists on this task")
        task.add_tag(normalized)
        return self._repo.save(task)

    def remove_task_tag(self, task_id: int, tag: str) -> Task:
        """Remove a tag from a task."""
        task = self.get_task(task_id)
        normalized = tag.strip().lower()
        if not task.has_tag(normalized):
            raise ValidationError(f"Tag '{tag}' not found on this task")
        task.remove_tag(normalized)
        return self._repo.save(task)

    def search_tasks(
        self,
        keyword: str,
        status: Optional[TaskStatus] = None,
        priority: Optional[Priority] = None,
        tag: Optional[str] = None
    ) -> list[Task]:
        """Search tasks by keyword, optionally filtered by status, priority, or tag."""
        keyword = keyword.lower()
        tasks = self._repo.get_all()

        # Keyword search in title or description
        if keyword:
            tasks = [
                t for t in tasks
                if keyword in t.title.lower()
                or (t.description and keyword in t.description.lower())
            ]

        # Apply filters (AND logic)
        if status:
            tasks = [t for t in tasks if t.status == status]
        if priority:
            tasks = [t for t in tasks if t.priority == priority]
        if tag:
            tag_lower = tag.strip().lower()
            tasks = [t for t in tasks if t.has_tag(tag_lower)]

        return sorted(tasks, key=lambda t: t.id)

    def filter_tasks(
        self,
        status: Optional[TaskStatus] = None,
        priority: Optional[Priority] = None,
        tag: Optional[str] = None
    ) -> list[Task]:
        """Filter tasks by optional criteria (AND logic)."""
        tasks = self._repo.get_all()

        if status:
            tasks = [t for t in tasks if t.status == status]
        if priority:
            tasks = [t for t in tasks if t.priority == priority]
        if tag:
            tag_lower = tag.strip().lower()
            tasks = [t for t in tasks if t.has_tag(tag_lower)]

        return sorted(tasks, key=lambda t: t.id)

    def sort_tasks(
        self,
        tasks: list[Task],
        field: str = "id",
        reverse: bool = False
    ) -> list[Task]:
        """Sort tasks by the specified field."""
        valid_fields = {"title", "priority", "id", "created"}
        if field not in valid_fields:
            raise ValidationError(
                f"Invalid sort field. Must be: {', '.join(sorted(valid_fields))}"
            )

        if field == "title":
            return sorted(tasks, key=lambda t: t.title.lower(), reverse=reverse)
        elif field == "priority":
            return sorted(tasks, key=lambda t: t.priority.sort_order, reverse=reverse)
        elif field == "created":
            return sorted(tasks, key=lambda t: t.created_at, reverse=reverse)
        else:  # id
            return sorted(tasks, key=lambda t: t.id, reverse=reverse)

    def delete_task(self, task_id: int) -> bool:
        """Delete a task."""
        if not self._repo.exists(task_id):
            raise TaskNotFoundError(task_id)
        return self._repo.delete(task_id)
