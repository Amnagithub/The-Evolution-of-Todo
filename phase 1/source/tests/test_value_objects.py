"""
Tests for domain value objects.
"""

import pytest
from todo.domain.value_objects import TaskStatus, Priority


class TestTaskStatus:
    """Tests for TaskStatus enum."""

    def test_pending_status_value(self):
        """PENDING status should have value 'pending'."""
        assert TaskStatus.PENDING.value == "pending"

    def test_completed_status_value(self):
        """COMPLETED status should have value 'completed'."""
        assert TaskStatus.COMPLETED.value == "completed"

    def test_from_string_pending(self):
        """from_string should return PENDING for 'pending'."""
        assert TaskStatus.from_string("pending") == TaskStatus.PENDING

    def test_from_string_completed(self):
        """from_string should return COMPLETED for 'completed'."""
        assert TaskStatus.from_string("completed") == TaskStatus.COMPLETED

    def test_from_string_case_insensitive(self):
        """from_string should be case-insensitive."""
        assert TaskStatus.from_string("COMPLETED") == TaskStatus.COMPLETED
        assert TaskStatus.from_string("Completed") == TaskStatus.COMPLETED
        assert TaskStatus.from_string("PENDING") == TaskStatus.PENDING

    def test_from_string_with_whitespace(self):
        """from_string should handle leading/trailing whitespace."""
        assert TaskStatus.from_string("  completed  ") == TaskStatus.COMPLETED
        assert TaskStatus.from_string("  pending  ") == TaskStatus.PENDING

    def test_from_string_default_to_pending(self):
        """from_string should default to PENDING for unknown values."""
        assert TaskStatus.from_string("unknown") == TaskStatus.PENDING

    def test_display_name_pending(self):
        """PENDING status should display as 'ACTIVE'."""
        assert TaskStatus.PENDING.display_name == "ACTIVE"

    def test_display_name_completed(self):
        """COMPLETED status should display as 'COMPLETED'."""
        assert TaskStatus.COMPLETED.display_name == "COMPLETED"


class TestPriority:
    """Tests for Priority enum."""

    def test_high_priority_value(self):
        """HIGH priority should have value 'HIGH'."""
        assert Priority.HIGH.value == "HIGH"

    def test_medium_priority_value(self):
        """MEDIUM priority should have value 'MEDIUM'."""
        assert Priority.MEDIUM.value == "MEDIUM"

    def test_low_priority_value(self):
        """LOW priority should have value 'LOW'."""
        assert Priority.LOW.value == "LOW"

    def test_from_string_high(self):
        """from_string should return HIGH for 'HIGH'."""
        assert Priority.from_string("HIGH") == Priority.HIGH

    def test_from_string_medium(self):
        """from_string should return MEDIUM for 'MEDIUM'."""
        assert Priority.from_string("MEDIUM") == Priority.MEDIUM

    def test_from_string_low(self):
        """from_string should return LOW for 'LOW'."""
        assert Priority.from_string("LOW") == Priority.LOW

    def test_from_string_case_insensitive(self):
        """from_string should be case-insensitive."""
        assert Priority.from_string("high") == Priority.HIGH
        assert Priority.from_string("High") == Priority.HIGH
        assert Priority.from_string("low") == Priority.LOW

    def test_from_string_with_whitespace(self):
        """from_string should handle leading/trailing whitespace."""
        assert Priority.from_string("  HIGH  ") == Priority.HIGH
        assert Priority.from_string("  low  ") == Priority.LOW

    def test_from_string_invalid_raises_error(self):
        """from_string should raise ValueError for invalid priority."""
        with pytest.raises(ValueError) as exc_info:
            Priority.from_string("invalid")
        assert "Invalid priority" in str(exc_info.value)
        assert "HIGH, MEDIUM, LOW" in str(exc_info.value)

    def test_sort_order_high(self):
        """HIGH priority should have sort order 0 (highest)."""
        assert Priority.HIGH.sort_order == 0

    def test_sort_order_medium(self):
        """MEDIUM priority should have sort order 1."""
        assert Priority.MEDIUM.sort_order == 1

    def test_sort_order_low(self):
        """LOW priority should have sort order 2 (lowest)."""
        assert Priority.LOW.sort_order == 2

    def test_sort_order_enables_correct_sorting(self):
        """sort_order should enable correct priority sorting."""
        priorities = [Priority.LOW, Priority.HIGH, Priority.MEDIUM]
        sorted_priorities = sorted(priorities, key=lambda p: p.sort_order)
        assert sorted_priorities == [Priority.HIGH, Priority.MEDIUM, Priority.LOW]
