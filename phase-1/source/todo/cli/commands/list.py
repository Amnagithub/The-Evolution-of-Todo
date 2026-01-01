"""
List command implementation.
"""

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
            print("No tasks found.")
            return 0

        # Format output
        if args.format == "json":
            self._print_json(tasks)
        elif args.format == "simple":
            self._print_simple(tasks)
        else:
            self._print_table(tasks)

        return 0

    def _print_table(self, tasks):
        """Print tasks in table format."""
        print("ID  | Title                    | Status    | Created")
        print("----|--------------------------|-----------|----------")
        for task in tasks:
            status = "Complete" if task.status.value == "completed" else "Incomplete"
            title = task.title[:24] + "..." if len(task.title) > 24 else task.title
            print(f"{task.id:<4}| {title:<24}| {status:<11}|")
        print(f"\nTotal: {len(tasks)} tasks")

    def _print_simple(self, tasks):
        """Print tasks in simple format."""
        for task in tasks:
            marker = "[✓]" if task.status.value == "completed" else "[ ]"
            print(f"{marker} #{task.id}: {task.title}")

    def _print_json(self, tasks):
        """Print tasks in JSON format."""
        import json
        data = [
            {
                "id": t.id,
                "title": t.title,
                "status": t.status.value,
                "created_at": t.created_at.isoformat()
            }
            for t in tasks
        ]
        print(json.dumps(data, indent=2))
