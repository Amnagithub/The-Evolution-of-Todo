"""
Pytest fixtures for todo tests.
"""

import pytest
from todo.domain.repository import InMemoryTaskRepository
from todo.services.task_service import TaskService


@pytest.fixture
def repository():
    """Create a fresh in-memory repository for each test."""
    return InMemoryTaskRepository()


@pytest.fixture
def service(repository):
    """Create a task service with a fresh repository for each test."""
    return TaskService(repository)


@pytest.fixture
def sample_task(service):
    """Create a sample task for tests that need pre-existing data."""
    return service.create_task("Sample task", description="A sample task for testing")


@pytest.fixture
def multiple_tasks(service):
    """Create multiple tasks for tests that need a populated list."""
    from todo.domain.value_objects import Priority

    tasks = [
        service.create_task("First task", priority=Priority.HIGH, tags=["urgent"]),
        service.create_task("Second task", description="With description", priority=Priority.MEDIUM),
        service.create_task("Third task", priority=Priority.LOW, tags=["work", "later"]),
    ]
    return tasks
