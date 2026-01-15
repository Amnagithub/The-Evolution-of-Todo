"""
Tests for domain repository.
"""

import pytest
from todo.domain.entities import Task
from todo.domain.repository import InMemoryTaskRepository


class TestInMemoryTaskRepository:
    """Tests for InMemoryTaskRepository."""

    def test_get_next_id_starts_at_one(self, repository):
        """get_next_id() should start at 1."""
        assert repository.get_next_id() == 1

    def test_get_next_id_increments(self, repository):
        """get_next_id() should increment on each call."""
        assert repository.get_next_id() == 1
        assert repository.get_next_id() == 2
        assert repository.get_next_id() == 3

    def test_save_stores_task(self, repository):
        """save() should store task in repository."""
        task = Task(id=1, title="Test task")
        repository.save(task)
        assert repository.get_by_id(1) is not None

    def test_save_returns_saved_task(self, repository):
        """save() should return the saved task."""
        task = Task(id=1, title="Test task")
        result = repository.save(task)
        assert result == task

    def test_save_updates_existing_task(self, repository):
        """save() should update existing task with same id."""
        task = Task(id=1, title="Original")
        repository.save(task)
        task.title = "Updated"
        repository.save(task)
        retrieved = repository.get_by_id(1)
        assert retrieved.title == "Updated"

    def test_get_by_id_returns_task(self, repository):
        """get_by_id() should return task with matching id."""
        task = Task(id=5, title="Test")
        repository.save(task)
        result = repository.get_by_id(5)
        assert result == task

    def test_get_by_id_returns_none_for_missing(self, repository):
        """get_by_id() should return None for non-existent id."""
        result = repository.get_by_id(999)
        assert result is None

    def test_get_all_returns_empty_list_initially(self, repository):
        """get_all() should return empty list when no tasks exist."""
        assert repository.get_all() == []

    def test_get_all_returns_all_tasks(self, repository):
        """get_all() should return all stored tasks."""
        task1 = Task(id=1, title="Task 1")
        task2 = Task(id=2, title="Task 2")
        repository.save(task1)
        repository.save(task2)
        result = repository.get_all()
        assert len(result) == 2
        assert task1 in result
        assert task2 in result

    def test_delete_removes_task(self, repository):
        """delete() should remove task from repository."""
        task = Task(id=1, title="Test")
        repository.save(task)
        repository.delete(1)
        assert repository.get_by_id(1) is None

    def test_delete_returns_true_on_success(self, repository):
        """delete() should return True when task is deleted."""
        task = Task(id=1, title="Test")
        repository.save(task)
        result = repository.delete(1)
        assert result is True

    def test_delete_returns_false_for_missing(self, repository):
        """delete() should return False for non-existent id."""
        result = repository.delete(999)
        assert result is False

    def test_exists_returns_true_for_existing_task(self, repository):
        """exists() should return True for existing task id."""
        task = Task(id=1, title="Test")
        repository.save(task)
        assert repository.exists(1) is True

    def test_exists_returns_false_for_missing(self, repository):
        """exists() should return False for non-existent id."""
        assert repository.exists(999) is False


class TestRepositoryIsolation:
    """Tests for repository isolation between tests."""

    def test_repository_starts_fresh(self, repository):
        """Each test should get a fresh repository instance."""
        assert repository.get_all() == []
        assert repository.get_next_id() == 1
