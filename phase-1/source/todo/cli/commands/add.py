"""
Add command implementation.
"""

import sys
from argparse import ArgumentParser, Namespace

from todo.cli.commands.base import Command
from todo.domain.errors import ValidationError
from todo.services.task_service import TaskService


class AddCommand(Command):
    """Command to add a new task."""

    def setup_parser(self, parser: ArgumentParser) -> None:
        """Configure argparse for add command."""
        parser.add_argument("title", help="Task title (required)")
        parser.add_argument(
            "description",
            nargs="?",
            default=None,
            help="Task description (optional)"
        )

    def execute(self, args: Namespace, service: TaskService) -> int:
        """Execute add command."""
        try:
            task = service.create_task(args.title, args.description)
            print(f"Task #{task.id} created: {task.title}")
            return 0
        except ValidationError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
