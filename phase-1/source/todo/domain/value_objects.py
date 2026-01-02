"""
Value objects for the todo domain.
"""

from enum import Enum


class TaskStatus(Enum):
    """Task status enumeration."""
    PENDING = "pending"
    COMPLETED = "completed"

    @classmethod
    def from_string(cls, status: str) -> "TaskStatus":
        """Create TaskStatus from string value."""
        status = status.lower().strip()
        if status == "completed":
            return cls.COMPLETED
        return cls.PENDING

    @property
    def display_name(self) -> str:
        """Return user-facing display name."""
        return "ACTIVE" if self == TaskStatus.PENDING else self.name


class Priority(Enum):
    """Task priority enumeration."""
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

    @classmethod
    def from_string(cls, priority: str) -> "Priority":
        """Create Priority from string value."""
        normalized = priority.strip().upper()
        try:
            return cls[normalized]
        except KeyError:
            raise ValueError(
                f"Invalid priority '{priority}'. "
                f"Must be one of: HIGH, MEDIUM, LOW"
            )

    @property
    def sort_order(self) -> int:
        """Return sort order (lower = higher priority)."""
        return {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}[self]
