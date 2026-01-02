"""
Sort command implementation.
"""

import sys
from argparse import ArgumentParser, Namespace

from todo.cli.commands.base import Command
from todo.domain.errors import ValidationError
from todo.services.task_service import TaskService


class SortCommand(Command):
    """Command to sort and display tasks."""

    def setup_parser(self, parser: ArgumentParser) -> None:
        """Configure argparse for sort command."""
        parser.add_argument(
            "field",
            choices=["title", "priority", "id", "created"],
            help="Field to sort by"
        )
        parser.add_argument(
            "--reverse",
            action="store_true",
            help="Sort in descending order instead of ascending"
        )

    def execute(self, args: Namespace, service: TaskService) -> int:
        """Execute sort command."""
        try:
            tasks = service.get_all_tasks()

            if not tasks:
                print("No tasks to sort.")
                return 0

            sorted_tasks = service.sort_tasks(tasks, field=args.field, reverse=args.reverse)

            order_desc = "descending" if args.reverse else "ascending"
            print(f"Sorted {len(tasks)} task(s) by: {args.field} ({order_desc}):\n")

            for task in sorted_tasks:
                tags_str = ", ".join(task.tags) if task.tags else ""
                print(f"[{task.id}] {task.priority.value} [{tags_str}] {task.title}")
                print(f"     id: {task.id} | status: {task.status.display_name} | priority: {task.priority.value} | tags: [{tags_str}]")
                print(f"     created: {task.created_at.strftime('%Y-%m-%d %H:%M')} | updated: {task.updated_at.strftime('%Y-%m-%d %H:%M')}")
                print()

            return 0
        except ValidationError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
