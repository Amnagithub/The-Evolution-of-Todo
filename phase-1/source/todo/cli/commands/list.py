"""
List command implementation.
"""

import json
from argparse import ArgumentParser, Namespace

from todo.cli.commands.base import Command
from todo.services.task_service import TaskService


class ListCommand(Command):
    """Command to list all tasks."""

    def setup_parser(self, parser: ArgumentParser) -> None:
        """Configure argparse for list command."""
        parser.add_argument(
            "--status",
            choices=["all", "pending", "completed"],
            default="all",
            help="Filter by status"
        )
        parser.add_argument(
            "--extended",
            action="store_true",
            help="Show full details including description, priority, and tags"
        )
        parser.add_argument(
            "--format",
            choices=["table", "simple", "json"],
            default="table",
            help="Output format"
        )

    def execute(self, args: Namespace, service: TaskService) -> int:
        """Execute list command."""
        tasks = service.get_all_tasks()

        # Filter by status
        if args.status == "pending":
            tasks = [t for t in tasks if t.status.value == "pending"]
        elif args.status == "completed":
            tasks = [t for t in tasks if t.status.value == "completed"]

        if not tasks:
            print("No tasks found. Use 'todo add <title>' to create a task.")
            print("\nShowing 0 task(s).")
            return 0

        # Extended output
        if args.extended:
            self._print_extended(tasks)
        else:
            # Format output
            if args.format == "json":
                self._print_json(tasks)
            elif args.format == "simple":
                self._print_simple(tasks)
            else:
                self._print_table(tasks)

        return 0

    def _print_table(self, tasks):
        """Print tasks in table format with priority and tags."""
        print("ID  Status    Priority  Title                      Tags")
        print("---- --------- --------- -------------------------- ---------------")
        for task in tasks:
            status = task.status.display_name
            priority = task.priority.value
            title = task.title[:24] + "..." if len(task.title) > 24 else task.title
            tags = ", ".join(task.tags) if task.tags else ""
            print(f"{task.id:<4} {status:<9} {priority:<9} {title:<24} {tags}")
        print(f"\nShowing {len(tasks)} task(s).")

    def _print_simple(self, tasks):
        """Print tasks in simple format."""
        for task in tasks:
            marker = "[✓]" if task.status.value == "completed" else "[ ]"
            priority = f"[{task.priority.value}]" if task.tags else ""
            print(f"{marker} #{task.id}: {priority} {task.title}".strip())

    def _print_json(self, tasks):
        """Print tasks in JSON format."""
        data = [
            {
                "id": t.id,
                "title": t.title,
                "description": t.description,
                "status": t.status.value,
                "priority": t.priority.value,
                "tags": t.tags,
                "created_at": t.created_at.isoformat(),
                "updated_at": t.updated_at.isoformat()
            }
            for t in tasks
        ]
        print(json.dumps(data, indent=2))

    def _print_extended(self, tasks):
        """Print tasks with full details."""
        print("ID  Status    Priority  Title                      Tags")
        print("---- --------- --------- -------------------------- ---------------")
        for task in tasks:
            status = task.status.display_name
            priority = task.priority.value
            title = task.title[:24] + "..." if len(task.title) > 24 else task.title
            tags = ", ".join(task.tags) if task.tags else ""
            print(f"{task.id:<4} {status:<9} {priority:<9} {title:<24} {tags}")

        print(f"\nShowing {len(tasks)} task(s).")

        print("\nTask Details:")
        for task in tasks:
            print(f"[{task.id}] {task.title}")
            if task.description:
                print(f"    Description: {task.description}")
            print(f"    Priority: {task.priority.value} | Tags: [{', '.join(task.tags) if task.tags else 'none'}]")
            print(f"    Created: {task.created_at.strftime('%Y-%m-%d %H:%M')} | Updated: {task.updated_at.strftime('%Y-%m-%d %H:%M')}")
            print(f"    Status: {task.status.display_name}")
            print()
