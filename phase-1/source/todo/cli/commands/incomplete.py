"""
Incomplete command implementation (reopen).
"""

import sys
from argparse import ArgumentParser, Namespace

from todo.cli.commands.base import Command
from todo.domain.errors import TaskNotFoundError
from todo.services.task_service import TaskService


class IncompleteCommand(Command):
    """Command to reopen a completed task."""

    def setup_parser(self, parser: ArgumentParser) -> None:
        """Configure argparse for incomplete command."""
        parser.add_argument(
            "task_id",
            type=int,
            help="Task ID to reopen"
        )
        parser.set_defaults(command_name="incomplete")

    def execute(self, args: Namespace, service: TaskService) -> int:
        """Execute incomplete command."""
        try:
            task = service.mark_task_incomplete(args.task_id)
            print(f"Task #{task.id} reopened")
            return 0
        except TaskNotFoundError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
