"""
Tests for domain entities.
"""

import pytest
from datetime import datetime, timezone
from todo.domain.entities import Task
from todo.domain.value_objects import TaskStatus, Priority


class TestTaskCreation:
    """Tests for Task entity creation."""

    def test_create_task_with_required_fields(self):
        """Task can be created with just id and title."""
        task = Task(id=1, title="My task")
        assert task.id == 1
        assert task.title == "My task"

    def test_default_description_is_none(self):
        """Task description defaults to None."""
        task = Task(id=1, title="Test")
        assert task.description is None

    def test_default_status_is_pending(self):
        """Task status defaults to PENDING."""
        task = Task(id=1, title="Test")
        assert task.status == TaskStatus.PENDING

    def test_default_priority_is_medium(self):
        """Task priority defaults to MEDIUM."""
        task = Task(id=1, title="Test")
        assert task.priority == Priority.MEDIUM

    def test_default_tags_is_empty_list(self):
        """Task tags defaults to empty list."""
        task = Task(id=1, title="Test")
        assert task.tags == []

    def test_timestamps_are_set_on_creation(self):
        """created_at and updated_at are set on creation."""
        task = Task(id=1, title="Test")
        assert isinstance(task.created_at, datetime)
        assert isinstance(task.updated_at, datetime)

    def test_create_task_with_all_fields(self):
        """Task can be created with all fields specified."""
        task = Task(
            id=1,
            title="Full task",
            description="A complete task",
            status=TaskStatus.COMPLETED,
            priority=Priority.HIGH,
            tags=["work", "urgent"]
        )
        assert task.id == 1
        assert task.title == "Full task"
        assert task.description == "A complete task"
        assert task.status == TaskStatus.COMPLETED
        assert task.priority == Priority.HIGH
        assert task.tags == ["work", "urgent"]


class TestTaskComplete:
    """Tests for Task.complete() method."""

    def test_complete_changes_status_to_completed(self):
        """complete() should change status to COMPLETED."""
        task = Task(id=1, title="Test")
        task.complete()
        assert task.status == TaskStatus.COMPLETED

    def test_complete_updates_timestamp(self):
        """complete() should update updated_at timestamp."""
        task = Task(id=1, title="Test")
        original_time = task.updated_at
        task.complete()
        assert task.updated_at >= original_time


class TestTaskReopen:
    """Tests for Task.reopen() method."""

    def test_reopen_changes_status_to_pending(self):
        """reopen() should change status to PENDING."""
        task = Task(id=1, title="Test", status=TaskStatus.COMPLETED)
        task.reopen()
        assert task.status == TaskStatus.PENDING

    def test_reopen_updates_timestamp(self):
        """reopen() should update updated_at timestamp."""
        task = Task(id=1, title="Test", status=TaskStatus.COMPLETED)
        original_time = task.updated_at
        task.reopen()
        assert task.updated_at >= original_time


class TestTaskUpdateTitle:
    """Tests for Task.update_title() method."""

    def test_update_title_changes_title(self):
        """update_title() should change the title."""
        task = Task(id=1, title="Original")
        task.update_title("Updated")
        assert task.title == "Updated"

    def test_update_title_updates_timestamp(self):
        """update_title() should update updated_at timestamp."""
        task = Task(id=1, title="Original")
        original_time = task.updated_at
        task.update_title("Updated")
        assert task.updated_at >= original_time


class TestTaskUpdateDescription:
    """Tests for Task.update_description() method."""

    def test_update_description_changes_description(self):
        """update_description() should change the description."""
        task = Task(id=1, title="Test")
        task.update_description("New description")
        assert task.description == "New description"

    def test_update_description_can_set_to_none(self):
        """update_description() should allow setting to None."""
        task = Task(id=1, title="Test", description="Has description")
        task.update_description(None)
        assert task.description is None

    def test_update_description_updates_timestamp(self):
        """update_description() should update updated_at timestamp."""
        task = Task(id=1, title="Test")
        original_time = task.updated_at
        task.update_description("New")
        assert task.updated_at >= original_time


class TestTaskUpdatePriority:
    """Tests for Task.update_priority() method."""

    def test_update_priority_changes_priority(self):
        """update_priority() should change the priority."""
        task = Task(id=1, title="Test")
        task.update_priority(Priority.HIGH)
        assert task.priority == Priority.HIGH

    def test_update_priority_updates_timestamp(self):
        """update_priority() should update updated_at timestamp."""
        task = Task(id=1, title="Test")
        original_time = task.updated_at
        task.update_priority(Priority.LOW)
        assert task.updated_at >= original_time


class TestTaskTags:
    """Tests for Task tag methods."""

    def test_add_tag_adds_new_tag(self):
        """add_tag() should add a new tag."""
        task = Task(id=1, title="Test")
        task.add_tag("work")
        assert "work" in task.tags

    def test_add_tag_normalizes_to_lowercase(self):
        """add_tag() should normalize tags to lowercase."""
        task = Task(id=1, title="Test")
        task.add_tag("WORK")
        assert "work" in task.tags
        assert "WORK" not in task.tags

    def test_add_tag_strips_whitespace(self):
        """add_tag() should strip whitespace from tags."""
        task = Task(id=1, title="Test")
        task.add_tag("  work  ")
        assert "work" in task.tags

    def test_add_tag_does_not_add_duplicates(self):
        """add_tag() should not add duplicate tags."""
        task = Task(id=1, title="Test", tags=["work"])
        task.add_tag("work")
        assert task.tags.count("work") == 1

    def test_add_tag_does_not_add_empty_tag(self):
        """add_tag() should not add empty or whitespace-only tags."""
        task = Task(id=1, title="Test")
        task.add_tag("")
        task.add_tag("   ")
        assert task.tags == []

    def test_add_tag_updates_timestamp(self):
        """add_tag() should update updated_at timestamp when tag is added."""
        task = Task(id=1, title="Test")
        original_time = task.updated_at
        task.add_tag("work")
        assert task.updated_at >= original_time

    def test_remove_tag_removes_existing_tag(self):
        """remove_tag() should remove an existing tag."""
        task = Task(id=1, title="Test", tags=["work"])
        result = task.remove_tag("work")
        assert result is True
        assert "work" not in task.tags

    def test_remove_tag_returns_false_for_missing_tag(self):
        """remove_tag() should return False for non-existent tag."""
        task = Task(id=1, title="Test")
        result = task.remove_tag("missing")
        assert result is False

    def test_remove_tag_is_case_insensitive(self):
        """remove_tag() should be case-insensitive."""
        task = Task(id=1, title="Test", tags=["work"])
        result = task.remove_tag("WORK")
        assert result is True
        assert "work" not in task.tags

    def test_has_tag_returns_true_for_existing_tag(self):
        """has_tag() should return True for existing tags."""
        task = Task(id=1, title="Test", tags=["work"])
        assert task.has_tag("work") is True

    def test_has_tag_returns_false_for_missing_tag(self):
        """has_tag() should return False for non-existent tags."""
        task = Task(id=1, title="Test")
        assert task.has_tag("work") is False

    def test_has_tag_is_case_insensitive(self):
        """has_tag() should be case-insensitive."""
        task = Task(id=1, title="Test", tags=["work"])
        assert task.has_tag("WORK") is True
        assert task.has_tag("Work") is True
