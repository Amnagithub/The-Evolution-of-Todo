"""
Domain errors for the todo application.
"""


class TodoError(Exception):
    """Base exception for todo domain errors."""
    pass


class TaskNotFoundError(TodoError):
    """Raised when a task is not found."""

    def __init__(self, task_id: int):
        self.task_id = task_id
        super().__init__(f"Task #{task_id} not found")


class ValidationError(TodoError):
    """Raised when validation fails."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)
