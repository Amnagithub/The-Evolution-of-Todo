"""
Main entry point for Todo CLI application.
"""

import sys
from argparse import ArgumentParser

from todo.cli.commands.add import AddCommand
from todo.cli.commands.list import ListCommand
from todo.cli.commands.complete import CompleteCommand
from todo.cli.commands.incomplete import IncompleteCommand
from todo.cli.commands.update import UpdateCommand
from todo.cli.commands.delete import DeleteCommand
from todo.cli.commands.help import HelpCommand
from todo.domain.repository import InMemoryTaskRepository
from todo.domain.errors import TaskNotFoundError, ValidationError
from todo.services.task_service import TaskService


def main():
    """Main entry point for CLI application."""
    parser = ArgumentParser(prog="todo", description="Manage your tasks")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Register all commands
    commands = [
        ("add", AddCommand()),
        ("list", ListCommand()),
        ("complete", CompleteCommand()),
        ("incomplete", IncompleteCommand(), ["reopen"]),
        ("update", UpdateCommand()),
        ("delete", DeleteCommand()),
        ("help", HelpCommand()),
    ]

    for name, cmd, *aliases in commands:
        cmd_parser = subparsers.add_parser(name, aliases=aliases if aliases else [])
        cmd.setup_parser(cmd_parser)
        cmd_parser.set_defaults(command_instance=cmd, command_name=name)

    args = parser.parse_args()

    # Initialize service
    repo = InMemoryTaskRepository()
    service = TaskService(repo)

    # Execute command
    command = args.command_instance
    exit_code = command.execute(args, service)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
