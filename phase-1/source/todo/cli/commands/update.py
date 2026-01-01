"""
Update command implementation.
"""

import sys
from argparse import ArgumentParser, Namespace

from todo.cli.commands.base import Command
from todo.domain.errors import TaskNotFoundError, ValidationError
from todo.services.task_service import TaskService


class UpdateCommand(Command):
    """Command to update a task."""

    def setup_parser(self, parser: ArgumentParser) -> None:
        """Configure argparse for update command."""
        parser.add_argument(
            "task_id",
            type=int,
            help="Task ID to update"
        )
        parser.add_argument(
            "--title",
            help="New task title"
        )
        parser.add_argument(
            "--desc",
            "--description",
            dest="description",
            help="New task description"
        )

    def execute(self, args: Namespace, service: TaskService) -> int:
        """Execute update command."""
        if not args.title and not args.description:
            print("Error: No fields to update", file=sys.stderr)
            return 1

        try:
            if args.title:
                service.update_task_title(args.task_id, args.title)
            if args.description is not None:
                service.update_task_description(args.task_id, args.description)
            print(f"Task #{args.task_id} updated")
            return 0
        except (TaskNotFoundError, ValidationError) as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
