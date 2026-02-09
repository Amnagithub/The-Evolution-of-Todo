"""
Delete command implementation.
"""

import sys
from argparse import ArgumentParser, Namespace

from todo.cli.commands.base import Command
from todo.domain.errors import TaskNotFoundError
from todo.services.task_service import TaskService


class DeleteCommand(Command):
    """Command to delete a task."""

    def setup_parser(self, parser: ArgumentParser) -> None:
        """Configure argparse for delete command."""
        parser.add_argument(
            "task_id",
            type=int,
            help="Task ID to delete"
        )

    def execute(self, args: Namespace, service: TaskService) -> int:
        """Execute delete command."""
        try:
            service.delete_task(args.task_id)
            print(f"Task #{args.task_id} deleted")
            return 0
        except TaskNotFoundError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
