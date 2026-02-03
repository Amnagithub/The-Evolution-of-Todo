"""
Add command implementation.
"""

import sys
from argparse import ArgumentParser, Namespace

from todo.cli.commands.base import Command
from todo.domain.errors import ValidationError
from todo.domain.value_objects import Priority
from todo.services.task_service import TaskService


class AddCommand(Command):
    """Command to add a new task."""

    def setup_parser(self, parser: ArgumentParser) -> None:
        """Configure argparse for add command."""
        parser.add_argument("title", help="Task title (required)")
        parser.add_argument(
            "--description",
            dest="description",
            default=None,
            help="Detailed task description (optional)"
        )
        parser.add_argument(
            "--priority",
            dest="priority",
            choices=["HIGH", "MEDIUM", "LOW"],
            default="MEDIUM",
            help="Priority level (default: MEDIUM)"
        )
        parser.add_argument(
            "--tag",
            dest="tags",
            action="append",
            default=[],
            help="Tag to add (can be specified multiple times)"
        )

    def execute(self, args: Namespace, service: TaskService) -> int:
        """Execute add command."""
        try:
            priority = Priority[args.priority]
            task = service.create_task(
                args.title,
                description=args.description,
                priority=priority,
                tags=args.tags if args.tags else None
            )
            tags_str = ", ".join(task.tags) if task.tags else "(none)"
            print(f"Task added: [{task.id}] {task.title}")
            print(f"     priority: {task.priority.value} | tags: [{tags_str}]")
            return 0
        except ValidationError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
        except KeyError:
            print(f"Error: Invalid priority '{args.priority}'. Must be HIGH, MEDIUM, or LOW.", file=sys.stderr)
            return 1
