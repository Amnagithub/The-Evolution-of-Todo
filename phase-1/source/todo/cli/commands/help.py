"""
Help command implementation.
"""

from argparse import ArgumentParser, Namespace

from todo.cli.commands.base import Command
from todo.services.task_service import TaskService


class HelpCommand(Command):
    """Command to display help."""

    def setup_parser(self, parser: ArgumentParser) -> None:
        """Configure argparse for help command."""
        parser.add_argument(
            "command",
            nargs="?",
            choices=["add", "list", "complete", "incomplete", "update", "delete"],
            help="Show help for a specific command"
        )

    def execute(self, args: Namespace, service: TaskService) -> int:
        """Execute help command."""
        if args.command == "add":
            print("Usage: todo add <title> [--desc <description>]")
            print("Create a new task with the given title.")
        elif args.command == "list":
            print("Usage: todo list [--status all|pending|complete] [--format table|simple|json]")
            print("Display all tasks with optional filtering.")
        elif args.command == "complete":
            print("Usage: todo complete <task-id>")
            print("Mark a task as complete.")
        elif args.command == "incomplete":
            print("Usage: todo incomplete <task-id>")
            print("Mark a task as incomplete (reopen).")
        elif args.command == "update":
            print("Usage: todo update <task-id> [--title <title>] [--desc <description>]")
            print("Update task title or description.")
        elif args.command == "delete":
            print("Usage: todo delete <task-id>")
            print("Permanently delete a task.")
        else:
            print("Todo - Manage your tasks from the terminal")
            print()
            print("Usage: todo <command> [options]")
            print()
            print("Available commands:")
            print("  add         Create a new task")
            print("  list        Display all tasks")
            print("  complete    Mark a task as complete")
            print("  incomplete  Mark a task as incomplete (reopen)")
            print("  update      Update task title or description")
            print("  delete      Delete a task permanently")
            print("  help        Show this help message")
            print()
            print("Run 'todo help <command>' for detailed help.")
        return 0
