"""
Tests for CLI commands.
"""

import json
import pytest
from argparse import Namespace
from io import StringIO
import sys

from todo.cli.commands.add import AddCommand
from todo.cli.commands.list import ListCommand
from todo.cli.commands.complete import CompleteCommand
from todo.cli.commands.incomplete import IncompleteCommand
from todo.cli.commands.update import UpdateCommand
from todo.cli.commands.delete import DeleteCommand
from todo.domain.value_objects import Priority, TaskStatus


class TestAddCommand:
    """Tests for AddCommand."""

    def test_add_command_creates_task(self, service, capsys):
        """AddCommand should create a task and print confirmation."""
        cmd = AddCommand()
        args = Namespace(title="New task", description=None, priority="MEDIUM", tags=[])
        exit_code = cmd.execute(args, service)

        assert exit_code == 0
        captured = capsys.readouterr()
        assert "Task added" in captured.out
        assert "New task" in captured.out

    def test_add_command_with_description(self, service, capsys):
        """AddCommand should accept description."""
        cmd = AddCommand()
        args = Namespace(title="Task", description="A description", priority="MEDIUM", tags=[])
        exit_code = cmd.execute(args, service)

        assert exit_code == 0
        task = service.get_task(1)
        assert task.description == "A description"

    def test_add_command_with_priority(self, service, capsys):
        """AddCommand should accept priority."""
        cmd = AddCommand()
        args = Namespace(title="Task", description=None, priority="HIGH", tags=[])
        exit_code = cmd.execute(args, service)

        assert exit_code == 0
        task = service.get_task(1)
        assert task.priority == Priority.HIGH

    def test_add_command_with_tags(self, service, capsys):
        """AddCommand should accept tags."""
        cmd = AddCommand()
        args = Namespace(title="Task", description=None, priority="MEDIUM", tags=["work", "urgent"])
        exit_code = cmd.execute(args, service)

        assert exit_code == 0
        task = service.get_task(1)
        assert "work" in task.tags
        assert "urgent" in task.tags

    def test_add_command_empty_title_returns_error(self, service, capsys):
        """AddCommand should return error for empty title."""
        cmd = AddCommand()
        args = Namespace(title="", description=None, priority="MEDIUM", tags=[])
        exit_code = cmd.execute(args, service)

        assert exit_code == 1
        captured = capsys.readouterr()
        assert "Error" in captured.err


class TestListCommand:
    """Tests for ListCommand."""

    def test_list_command_empty(self, service, capsys):
        """ListCommand should show message when no tasks."""
        cmd = ListCommand()
        args = Namespace(status="all", extended=False, format="table")
        exit_code = cmd.execute(args, service)

        assert exit_code == 0
        captured = capsys.readouterr()
        assert "No tasks found" in captured.out

    def test_list_command_shows_tasks(self, service, multiple_tasks, capsys):
        """ListCommand should list all tasks."""
        cmd = ListCommand()
        args = Namespace(status="all", extended=False, format="table")
        exit_code = cmd.execute(args, service)

        assert exit_code == 0
        captured = capsys.readouterr()
        assert "First task" in captured.out
        assert "Second task" in captured.out
        assert "Third task" in captured.out
        assert "3 task(s)" in captured.out

    def test_list_command_filter_pending(self, service, multiple_tasks, capsys):
        """ListCommand should filter by pending status."""
        service.mark_task_complete(multiple_tasks[0].id)
        cmd = ListCommand()
        args = Namespace(status="pending", extended=False, format="table")
        exit_code = cmd.execute(args, service)

        assert exit_code == 0
        captured = capsys.readouterr()
        assert "First task" not in captured.out
        assert "2 task(s)" in captured.out

    def test_list_command_filter_completed(self, service, multiple_tasks, capsys):
        """ListCommand should filter by completed status."""
        service.mark_task_complete(multiple_tasks[0].id)
        cmd = ListCommand()
        args = Namespace(status="completed", extended=False, format="table")
        exit_code = cmd.execute(args, service)

        assert exit_code == 0
        captured = capsys.readouterr()
        assert "First task" in captured.out
        assert "1 task(s)" in captured.out

    def test_list_command_simple_format(self, service, multiple_tasks, capsys):
        """ListCommand should output simple format."""
        cmd = ListCommand()
        args = Namespace(status="all", extended=False, format="simple")
        exit_code = cmd.execute(args, service)

        assert exit_code == 0
        captured = capsys.readouterr()
        assert "[ ]" in captured.out
        assert "#1" in captured.out

    def test_list_command_json_format(self, service, multiple_tasks, capsys):
        """ListCommand should output JSON format."""
        cmd = ListCommand()
        args = Namespace(status="all", extended=False, format="json")
        exit_code = cmd.execute(args, service)

        assert exit_code == 0
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert len(data) == 3
        assert data[0]["title"] == "First task"

    def test_list_command_extended(self, service, multiple_tasks, capsys):
        """ListCommand should show extended details."""
        cmd = ListCommand()
        args = Namespace(status="all", extended=True, format="table")
        exit_code = cmd.execute(args, service)

        assert exit_code == 0
        captured = capsys.readouterr()
        assert "Task Details:" in captured.out


class TestCompleteCommand:
    """Tests for CompleteCommand."""

    def test_complete_command_marks_complete(self, service, sample_task, capsys):
        """CompleteCommand should mark task as complete."""
        cmd = CompleteCommand()
        args = Namespace(task_id=sample_task.id)
        exit_code = cmd.execute(args, service)

        assert exit_code == 0
        captured = capsys.readouterr()
        assert "marked complete" in captured.out
        task = service.get_task(sample_task.id)
        assert task.status == TaskStatus.COMPLETED

    def test_complete_command_not_found(self, service, capsys):
        """CompleteCommand should return error for missing task."""
        cmd = CompleteCommand()
        args = Namespace(task_id=999)
        exit_code = cmd.execute(args, service)

        assert exit_code == 1
        captured = capsys.readouterr()
        assert "Error" in captured.err


class TestIncompleteCommand:
    """Tests for IncompleteCommand."""

    def test_incomplete_command_marks_incomplete(self, service, sample_task, capsys):
        """IncompleteCommand should mark task as incomplete."""
        from todo.cli.commands.incomplete import IncompleteCommand

        service.mark_task_complete(sample_task.id)
        cmd = IncompleteCommand()
        args = Namespace(task_id=sample_task.id)
        exit_code = cmd.execute(args, service)

        assert exit_code == 0
        captured = capsys.readouterr()
        assert "reopened" in captured.out
        task = service.get_task(sample_task.id)
        assert task.status == TaskStatus.PENDING


class TestUpdateCommand:
    """Tests for UpdateCommand."""

    def test_update_command_updates_title(self, service, sample_task, capsys):
        """UpdateCommand should update task title."""
        cmd = UpdateCommand()
        args = Namespace(task_id=sample_task.id, title="Updated title", description=None, priority=None, add_tags=[], remove_tags=[])
        exit_code = cmd.execute(args, service)

        assert exit_code == 0
        captured = capsys.readouterr()
        assert "updated" in captured.out.lower()
        task = service.get_task(sample_task.id)
        assert task.title == "Updated title"

    def test_update_command_updates_description(self, service, sample_task, capsys):
        """UpdateCommand should update task description."""
        cmd = UpdateCommand()
        args = Namespace(task_id=sample_task.id, title=None, description="New description", priority=None, add_tags=[], remove_tags=[])
        exit_code = cmd.execute(args, service)

        assert exit_code == 0
        task = service.get_task(sample_task.id)
        assert task.description == "New description"

    def test_update_command_updates_priority(self, service, sample_task, capsys):
        """UpdateCommand should update task priority."""
        cmd = UpdateCommand()
        args = Namespace(task_id=sample_task.id, title=None, description=None, priority="HIGH", add_tags=[], remove_tags=[])
        exit_code = cmd.execute(args, service)

        assert exit_code == 0
        task = service.get_task(sample_task.id)
        assert task.priority == Priority.HIGH

    def test_update_command_not_found(self, service, capsys):
        """UpdateCommand should return error for missing task."""
        cmd = UpdateCommand()
        args = Namespace(task_id=999, title="Test", description=None, priority=None, add_tags=[], remove_tags=[])
        exit_code = cmd.execute(args, service)

        assert exit_code == 1
        captured = capsys.readouterr()
        assert "Error" in captured.err


class TestDeleteCommand:
    """Tests for DeleteCommand."""

    def test_delete_command_deletes_task(self, service, sample_task, capsys):
        """DeleteCommand should delete task."""
        cmd = DeleteCommand()
        args = Namespace(task_id=sample_task.id)
        exit_code = cmd.execute(args, service)

        assert exit_code == 0
        captured = capsys.readouterr()
        assert "deleted" in captured.out
        assert service.get_all_tasks() == []

    def test_delete_command_not_found(self, service, capsys):
        """DeleteCommand should return error for missing task."""
        cmd = DeleteCommand()
        args = Namespace(task_id=999)
        exit_code = cmd.execute(args, service)

        assert exit_code == 1
        captured = capsys.readouterr()
        assert "Error" in captured.err
