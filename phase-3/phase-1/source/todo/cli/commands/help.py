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
            choices=["add", "list", "search", "filter", "sort", "complete", "incomplete", "update", "delete", "help"],
            help="Show help for a specific command"
        )

    def execute(self, args: Namespace, service: TaskService) -> int:
        """Execute help command."""
        if args.command == "add":
            print("Usage: todo add <title> [--description <desc>] [--priority HIGH|MEDIUM|LOW>] [--tag <tag>]")
            print("Create a new task with the given title.")
            print()
            print("Options:")
            print("  --description DESC  Detailed task description (optional)")
            print("  --priority LEVEL    Priority level: HIGH, MEDIUM, LOW (default: MEDIUM)")
            print("  --tag TAG           Tag to add (can be specified multiple times)")
        elif args.command == "list":
            print("Usage: todo list [--status all|pending|complete] [--extended] [--format table|simple|json]")
            print("Display all tasks with optional filtering.")
            print()
            print("Options:")
            print("  --status FILTER   Filter by status: all, pending, completed")
            print("  --extended        Show full details including description, priority, and tags")
            print("  --format FORMAT   Output format: table, simple, json")
        elif args.command == "search":
            print("Usage: todo search <keyword> [--status ACTIVE|COMPLETED] [--priority HIGH|MEDIUM|LOW>] [--tag <tag>]")
            print("Search for tasks containing the keyword in title or description.")
            print()
            print("Options:")
            print("  keyword           Text to search for (required)")
            print("  --status          Filter by task status")
            print("  --priority        Filter by priority level")
            print("  --tag             Filter by specific tag")
        elif args.command == "filter":
            print("Usage: todo filter [--status ACTIVE|COMPLETED] [--priority HIGH|MEDIUM|LOW>] [--tag <tag>]")
            print("Filter tasks by criteria (multiple filters use AND logic).")
            print()
            print("Options:")
            print("  --status          Show only tasks with specific status")
            print("  --priority        Show only tasks with specific priority")
            print("  --tag             Show only tasks with specific tag")
        elif args.command == "sort":
            print("Usage: todo sort <field> [--reverse]")
            print("Display tasks sorted by the specified field.")
            print()
            print("Arguments:")
            print("  field             Sort by: title, priority, id, created")
            print()
            print("Options:")
            print("  --reverse         Sort in descending order instead of ascending")
        elif args.command == "complete":
            print("Usage: todo complete <task-id>")
            print("Mark a task as complete.")
        elif args.command == "incomplete":
            print("Usage: todo incomplete <task-id>")
            print("Mark a task as incomplete (reopen).")
        elif args.command == "update":
            print("Usage: todo update <task-id> [--title <title>] [--description <desc>] [--priority HIGH|MEDIUM|LOW>] [--add-tag <tag>] [--remove-tag <tag>]")
            print("Update task properties.")
            print()
            print("Options:")
            print("  --title           New task title")
            print("  --description     New task description (empty string to clear)")
            print("  --priority        Update priority level")
            print("  --add-tag         Add a tag (can be specified multiple times)")
            print("  --remove-tag      Remove a tag (can be specified multiple times)")
        elif args.command == "delete":
            print("Usage: todo delete <task-id>")
            print("Permanently delete a task.")
        elif args.command == "help":
            print("Usage: todo help [command]")
            print("Show help for a specific command or list all commands.")
        else:
            print("Todo - Manage your tasks from the terminal")
            print()
            print("Usage: todo <command> [options]")
            print()
            print("Available commands:")
            print("  add         Create a new task")
            print("  list        Display all tasks")
            print("  search      Search tasks by keyword")
            print("  filter      Filter tasks by criteria")
            print("  sort        Sort tasks by field")
            print("  complete    Mark a task as complete")
            print("  incomplete  Mark a task as incomplete (reopen)")
            print("  update      Update task properties")
            print("  delete      Delete a task permanently")
            print("  help        Show this help message")
            print()
            print("Run 'todo help <command>' for detailed help.")
        return 0
