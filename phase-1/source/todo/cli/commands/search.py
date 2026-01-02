"""
Search command implementation.
"""

import sys
from argparse import ArgumentParser, Namespace

from todo.cli.commands.base import Command
from todo.domain.errors import ValidationError
from todo.domain.value_objects import Priority, TaskStatus
from todo.services.task_service import TaskService


class SearchCommand(Command):
    """Command to search tasks by keyword."""

    def setup_parser(self, parser: ArgumentParser) -> None:
        """Configure argparse for search command."""
        parser.add_argument(
            "keyword",
            help="Keyword to search for in title and description"
        )
        parser.add_argument(
            "--status",
            choices=["ACTIVE", "COMPLETED"],
            help="Filter by task status"
        )
        parser.add_argument(
            "--priority",
            choices=["HIGH", "MEDIUM", "LOW"],
            help="Filter by priority level"
        )
        parser.add_argument(
            "--tag",
            help="Filter by specific tag"
        )

    def execute(self, args: Namespace, service: TaskService) -> int:
        """Execute search command."""
        try:
            # Convert string arguments to enums
            status = None
            if args.status:
                status = TaskStatus.COMPLETED if args.status == "COMPLETED" else TaskStatus.PENDING

            priority = None
            if args.priority:
                priority = Priority[args.priority]

            tag = args.tag

            tasks = service.search_tasks(args.keyword, status=status, priority=priority, tag=tag)

            if not tasks:
                print(f"No tasks found matching '{args.keyword}'.")
                return 0

            # Build filter description
            filters = []
            if status:
                filters.append(f"status={status.display_name}")
            if priority:
                filters.append(f"priority={priority.value}")
            if tag:
                filters.append(f"tag={tag}")

            filter_desc = ""
            if filters:
                filter_desc = " (" + ", ".join(filters) + ")"

            print(f"Found {len(tasks)} task(s) matching \"{args.keyword}\"{filter_desc}:\n")

            for task in tasks:
                tags_str = ", ".join(task.tags) if task.tags else ""
                print(f"[{task.id}] {task.priority.value} [{tags_str}] {task.title}")
                print(f"     id: {task.id} | status: {task.status.display_name} | priority: {task.priority.value} | tags: [{tags_str}]")
                print(f"     created: {task.created_at.strftime('%Y-%m-%d %H:%M')} | updated: {task.updated_at.strftime('%Y-%m-%d %H:%M')}")
                print()

            return 0
        except ValidationError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
        except KeyError:
            print(f"Error: Invalid priority '{args.priority}'. Must be HIGH, MEDIUM, or LOW.", file=sys.stderr)
            return 1
