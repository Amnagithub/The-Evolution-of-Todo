"""
Complete command implementation.
"""

import sys
from argparse import ArgumentParser, Namespace

from todo.cli.commands.base import Command
from todo.domain.errors import TaskNotFoundError
from todo.services.task_service import TaskService


class CompleteCommand(Command):
    """Command to mark a task as complete."""

    def setup_parser(self, parser: ArgumentParser) -> None:
        """Configure argparse for complete command."""
        parser.add_argument(
            "task_id",
            type=int,
            help="Task ID to mark as complete"
        )

    def execute(self, args: Namespace, service: TaskService) -> int:
        """Execute complete command."""
        try:
            task = service.mark_task_complete(args.task_id)
            print(f"Task #{task.id} marked complete")
            return 0
        except TaskNotFoundError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
