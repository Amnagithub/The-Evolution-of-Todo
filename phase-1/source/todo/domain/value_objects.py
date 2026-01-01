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
