"""
Tests for domain errors.
"""

import pytest
from todo.domain.errors import TodoError, TaskNotFoundError, ValidationError


class TestTodoError:
    """Tests for base TodoError exception."""

    def test_todo_error_is_exception(self):
        """TodoError should be an Exception subclass."""
        assert issubclass(TodoError, Exception)

    def test_todo_error_can_be_raised(self):
        """TodoError should be raiseable."""
        with pytest.raises(TodoError):
            raise TodoError("Test error")


class TestTaskNotFoundError:
    """Tests for TaskNotFoundError exception."""

    def test_inherits_from_todo_error(self):
        """TaskNotFoundError should inherit from TodoError."""
        assert issubclass(TaskNotFoundError, TodoError)

    def test_stores_task_id(self):
        """TaskNotFoundError should store the task_id."""
        error = TaskNotFoundError(42)
        assert error.task_id == 42

    def test_message_includes_task_id(self):
        """TaskNotFoundError message should include task id."""
        error = TaskNotFoundError(42)
        assert "42" in str(error)
        assert "not found" in str(error).lower()


class TestValidationError:
    """Tests for ValidationError exception."""

    def test_inherits_from_todo_error(self):
        """ValidationError should inherit from TodoError."""
        assert issubclass(ValidationError, TodoError)

    def test_stores_message(self):
        """ValidationError should store the message."""
        error = ValidationError("Invalid input")
        assert error.message == "Invalid input"

    def test_str_returns_message(self):
        """ValidationError str should return the message."""
        error = ValidationError("Invalid input")
        assert str(error) == "Invalid input"
