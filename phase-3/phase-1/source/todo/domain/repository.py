"""
In-memory repository for tasks.
"""

from typing import Optional, Protocol, runtime_checkable

from todo.domain.entities import Task


@runtime_checkable
class TaskRepository(Protocol):
    """Protocol for task repository operations."""

    def save(self, task: Task) -> Task: ...
    def get_by_id(self, task_id: int) -> Optional[Task]: ...
    def get_all(self) -> list[Task]: ...
    def delete(self, task_id: int) -> bool: ...
    def exists(self, task_id: int) -> bool: ...
    def get_next_id(self) -> int: ...


class InMemoryTaskRepository:
    """In-memory storage for tasks using dictionary."""

    def __init__(self):
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    def save(self, task: Task) -> Task:
        """Save a task to the repository."""
        self._tasks[task.id] = task
        return task

    def get_by_id(self, task_id: int) -> Optional[Task]:
        """Retrieve a task by its ID."""
        return self._tasks.get(task_id)

    def get_all(self) -> list[Task]:
        """Retrieve all tasks."""
        return list(self._tasks.values())

    def delete(self, task_id: int) -> bool:
        """Delete a task from the repository."""
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def exists(self, task_id: int) -> bool:
        """Check if a task exists."""
        return task_id in self._tasks

    def get_next_id(self) -> int:
        """Generate the next available task ID."""
        next_id = self._next_id
        self._next_id += 1
        return next_id
