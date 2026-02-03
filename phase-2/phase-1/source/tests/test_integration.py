"""
Integration tests for complete workflows.
"""

import pytest
from todo.domain.repository import InMemoryTaskRepository
from todo.services.task_service import TaskService
from todo.domain.value_objects import Priority, TaskStatus


class TestTaskLifecycle:
    """Integration tests for complete task lifecycle."""

    def test_create_complete_delete_workflow(self, service):
        """Test full task lifecycle: create -> complete -> delete."""
        # Create task
        task = service.create_task("My task", description="A test task")
        assert task.id == 1
        assert task.status == TaskStatus.PENDING

        # Complete task
        service.mark_task_complete(task.id)
        task = service.get_task(task.id)
        assert task.status == TaskStatus.COMPLETED

        # Delete task
        service.delete_task(task.id)
        assert service.get_all_tasks() == []

    def test_create_update_reopen_workflow(self, service):
        """Test task update and reopen workflow."""
        # Create task
        task = service.create_task("Original title")
        original_id = task.id

        # Update title and description
        service.update_task_title(task.id, "Updated title")
        service.update_task_description(task.id, "New description")
        service.update_task_priority(task.id, Priority.HIGH)

        # Verify updates
        task = service.get_task(original_id)
        assert task.title == "Updated title"
        assert task.description == "New description"
        assert task.priority == Priority.HIGH

        # Complete and reopen
        service.mark_task_complete(task.id)
        assert service.get_task(task.id).status == TaskStatus.COMPLETED

        service.mark_task_incomplete(task.id)
        assert service.get_task(task.id).status == TaskStatus.PENDING

    def test_multiple_tasks_filter_sort_workflow(self, service):
        """Test filtering and sorting multiple tasks."""
        # Create multiple tasks with different properties
        task1 = service.create_task("Alpha task", priority=Priority.LOW)
        task2 = service.create_task("Beta task", priority=Priority.HIGH, tags=["urgent"])
        task3 = service.create_task("Gamma task", priority=Priority.MEDIUM, tags=["work"])
        task4 = service.create_task("Delta task", priority=Priority.HIGH)

        # Complete some tasks
        service.mark_task_complete(task1.id)
        service.mark_task_complete(task3.id)

        # Filter by status
        pending = service.filter_tasks(status=TaskStatus.PENDING)
        assert len(pending) == 2
        assert all(t.status == TaskStatus.PENDING for t in pending)

        completed = service.filter_tasks(status=TaskStatus.COMPLETED)
        assert len(completed) == 2

        # Filter by priority
        high_priority = service.filter_tasks(priority=Priority.HIGH)
        assert len(high_priority) == 2

        # Filter by tag
        urgent = service.filter_tasks(tag="urgent")
        assert len(urgent) == 1
        assert urgent[0].title == "Beta task"

        # Sort by priority
        all_tasks = service.get_all_tasks()
        sorted_by_priority = service.sort_tasks(all_tasks, field="priority")
        assert sorted_by_priority[0].priority == Priority.HIGH
        assert sorted_by_priority[-1].priority == Priority.LOW

        # Sort by title
        sorted_by_title = service.sort_tasks(all_tasks, field="title")
        assert sorted_by_title[0].title == "Alpha task"
        assert sorted_by_title[-1].title == "Gamma task"


class TestSearchWorkflow:
    """Integration tests for search functionality."""

    def test_search_across_title_and_description(self, service):
        """Test searching across title and description."""
        service.create_task("Buy groceries", description="Milk, eggs, bread")
        service.create_task("Call mom", description="Discuss groceries for party")
        service.create_task("Write report", description="Quarterly sales report")

        # Search for "groceries"
        results = service.search_tasks("groceries")
        assert len(results) == 2

        # Search for "report"
        results = service.search_tasks("report")
        assert len(results) == 1
        assert results[0].title == "Write report"

    def test_search_with_filters(self, service):
        """Test search combined with filters."""
        task1 = service.create_task("Urgent task", priority=Priority.HIGH, tags=["work"])
        task2 = service.create_task("Another urgent item", priority=Priority.LOW)
        task3 = service.create_task("Completed task", priority=Priority.HIGH)

        service.mark_task_complete(task3.id)

        # Search "urgent" with pending status
        results = service.search_tasks("urgent", status=TaskStatus.PENDING)
        assert len(results) == 2

        # Search "urgent" with HIGH priority - only task1 matches both
        results = service.search_tasks("urgent", priority=Priority.HIGH)
        assert len(results) == 1
        assert results[0].title == "Urgent task"

        # Search with tag filter
        results = service.search_tasks("urgent", tag="work")
        assert len(results) == 1


class TestTagWorkflow:
    """Integration tests for tag operations."""

    def test_tag_management_workflow(self, service):
        """Test adding, removing, and filtering by tags."""
        # Create task with initial tags
        task = service.create_task("Tagged task", tags=["work", "important"])

        # Add more tags
        service.add_task_tag(task.id, "urgent")
        task = service.get_task(task.id)
        assert len(task.tags) == 3
        assert "urgent" in task.tags

        # Filter by tag
        work_tasks = service.filter_tasks(tag="work")
        assert len(work_tasks) == 1

        # Remove tag
        service.remove_task_tag(task.id, "work")
        work_tasks = service.filter_tasks(tag="work")
        assert len(work_tasks) == 0

        # Verify remaining tags
        task = service.get_task(task.id)
        assert "work" not in task.tags
        assert "important" in task.tags
        assert "urgent" in task.tags


class TestRepositoryPersistence:
    """Tests for repository state persistence within session."""

    def test_repository_maintains_state(self, repository):
        """Repository should maintain state across operations."""
        from todo.domain.entities import Task

        # Add multiple tasks
        for i in range(5):
            task = Task(id=repository.get_next_id(), title=f"Task {i+1}")
            repository.save(task)

        # Verify all tasks are stored
        assert len(repository.get_all()) == 5

        # Delete some tasks
        repository.delete(2)
        repository.delete(4)

        # Verify deletions
        assert len(repository.get_all()) == 3
        assert repository.get_by_id(2) is None
        assert repository.get_by_id(4) is None
        assert repository.get_by_id(1) is not None
        assert repository.get_by_id(3) is not None

    def test_id_generation_after_deletions(self, service):
        """ID generation should continue incrementing after deletions."""
        task1 = service.create_task("Task 1")  # ID 1
        task2 = service.create_task("Task 2")  # ID 2
        task3 = service.create_task("Task 3")  # ID 3

        service.delete_task(task2.id)

        # New task should get ID 4, not reuse ID 2
        task4 = service.create_task("Task 4")
        assert task4.id == 4


class TestEdgeCases:
    """Integration tests for edge cases."""

    def test_empty_repository_operations(self, service):
        """Operations on empty repository should behave correctly."""
        assert service.get_all_tasks() == []
        assert service.filter_tasks() == []
        assert service.search_tasks("anything") == []

    def test_boundary_values(self, service):
        """Test with boundary values for title and description."""
        # Max title length (200 chars)
        long_title = "x" * 200
        task = service.create_task(long_title)
        assert len(task.title) == 200

        # Max description length (2000 chars)
        long_desc = "y" * 2000
        task = service.create_task("Test", description=long_desc)
        assert len(task.description) == 2000

        # Max tag length (50 chars)
        long_tag = "z" * 50
        task = service.create_task("Test", tags=[long_tag])
        assert long_tag in task.tags

    def test_special_characters_in_content(self, service):
        """Test handling of special characters."""
        task = service.create_task(
            "Task with special chars: @#$%^&*()",
            description="Description with unicode: test",
            tags=["tag-with-dashes", "tag_with_underscores"]
        )
        assert "@#$%^&*()" in task.title
        assert "tag-with-dashes" in task.tags
