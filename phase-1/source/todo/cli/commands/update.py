"""
Update command implementation.
"""

import sys
from argparse import ArgumentParser, Namespace

from todo.cli.commands.base import Command
from todo.domain.errors import TaskNotFoundError, ValidationError
from todo.domain.value_objects import Priority
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
            "--description",
            "--desc",
            dest="description",
            help="New task description (use empty string to clear)"
        )
        parser.add_argument(
            "--priority",
            choices=["HIGH", "MEDIUM", "LOW"],
            help="Update priority level"
        )
        parser.add_argument(
            "--add-tag",
            dest="add_tags",
            action="append",
            default=[],
            help="Add a tag (can be specified multiple times)"
        )
        parser.add_argument(
            "--remove-tag",
            dest="remove_tags",
            action="append",
            default=[],
            help="Remove a tag (can be specified multiple times)"
        )

    def execute(self, args: Namespace, service: TaskService) -> int:
        """Execute update command."""
        if not any([args.title, args.description is not None, args.priority, args.add_tags, args.remove_tags]):
            print("Error: No fields to update", file=sys.stderr)
            return 1

        try:
            # Get current task to show changes
            task = service.get_task(args.task_id)
            changes = []

            if args.title:
                service.update_task_title(args.task_id, args.title)
                changes.append(f"title")

            if args.description is not None:
                service.update_task_description(args.task_id, args.description)
                changes.append("description")

            if args.priority:
                old_priority = task.priority.value
                service.update_task_priority(args.task_id, Priority[args.priority])
                changes.append(f"priority: {old_priority} -> {args.priority}")

            for tag in args.add_tags:
                service.add_task_tag(args.task_id, tag)
                changes.append(f"added tag: {tag}")

            for tag in args.remove_tags:
                service.remove_task_tag(args.task_id, tag)
                changes.append(f"removed tag: {tag}")

            # Get updated task for display
            updated_task = service.get_task(args.task_id)

            print(f"Task updated: [{updated_task.id}] {updated_task.title}")
            if changes:
                print(f"     Changes: {', '.join(changes)}")
            print(f"     priority: {updated_task.priority.value} | tags: [{', '.join(updated_task.tags) if updated_task.tags else 'none'}]")
            return 0
        except (TaskNotFoundError, ValidationError) as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
        except KeyError:
            print(f"Error: Invalid priority '{args.priority}'. Must be HIGH, MEDIUM, or LOW.", file=sys.stderr)
            return 1
