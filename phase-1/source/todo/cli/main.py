"""
Main entry point for Todo CLI application.
"""

import sys
import shlex
import signal
from argparse import ArgumentParser, Namespace

from todo.cli.commands.add import AddCommand
from todo.cli.commands.list import ListCommand
from todo.cli.commands.complete import CompleteCommand
from todo.cli.commands.incomplete import IncompleteCommand
from todo.cli.commands.update import UpdateCommand
from todo.cli.commands.delete import DeleteCommand
from todo.cli.commands.help import HelpCommand
from todo.cli.commands.search import SearchCommand
from todo.cli.commands.filter import FilterCommand
from todo.cli.commands.sort import SortCommand
from todo.domain.repository import InMemoryTaskRepository
from todo.domain.errors import TaskNotFoundError, ValidationError
from todo.services.task_service import TaskService


def _create_parser() -> tuple[ArgumentParser, dict]:
    """Create and configure ArgumentParser with all command subparsers.

    Returns:
        Tuple of (parser, commands_dict) where commands_dict maps command names to instances.
    """
    parser = ArgumentParser(prog="todo", description="Manage your tasks")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Register all commands
    commands = [
        ("add", AddCommand()),
        ("list", ListCommand()),
        ("search", SearchCommand()),
        ("filter", FilterCommand()),
        ("sort", SortCommand()),
        ("complete", CompleteCommand()),
        ("incomplete", IncompleteCommand(), ["reopen"]),
        ("update", UpdateCommand()),
        ("delete", DeleteCommand()),
        ("help", HelpCommand()),
    ]

    commands_dict = {}
    for name, cmd, *aliases in commands:
        kwargs = {"aliases": aliases[0]} if aliases else {}
        cmd_parser = subparsers.add_parser(name, **kwargs)
        cmd.setup_parser(cmd_parser)
        cmd_parser.set_defaults(command_instance=cmd, command_name=name)
        commands_dict[name] = cmd

    return parser, commands_dict


def _execute_command(args: Namespace, service: TaskService, commands_dict: dict) -> int:
    """Execute a command using the parsed arguments and shared service.

    Args:
        args: Parsed argument namespace
        service: Shared TaskService instance
        commands_dict: Dictionary mapping command names to command instances

    Returns:
        Exit code from command execution
    """
    command = args.command_instance
    return command.execute(args, service)


def _start_interactive_session(service: TaskService, commands_dict: dict) -> None:
    """Start the interactive session loop.

    Args:
        service: Shared TaskService instance for the session
        commands_dict: Dictionary mapping command names to command instances
    """
    print("Todo CLI - Interactive Session")
    print("Type 'exit' or 'quit' to end the session.\n")

    while True:
        try:
            line = sys.stdin.readline()
            if line == "":
                # EOF received (Ctrl+D)
                print("\nSession ended.")
                break

            line = line.strip()

            # Handle empty lines
            if not line:
                continue

            # Handle exit commands
            if line.lower() in ("exit", "quit"):
                print("Goodbye!")
                break

            # Parse the command line
            try:
                parts = shlex.split(line)
            except ValueError as e:
                print(f"Error parsing command: {e}")
                continue

            if not parts:
                continue

            command_name = parts[0]
            args_parts = ["todo"] + parts  # Prefix with program name for argparse

            # Check for valid command
            if command_name not in commands_dict:
                print(f"Unknown command: {command_name}")
                print("Available commands: add, list, search, filter, sort, complete, incomplete, update, delete, help")
                continue

            # Create parser and parse arguments
            parser, _ = _create_parser()
            try:
                args = parser.parse_args(args_parts[1:])
            except SystemExit:
                continue

            # Execute the command
            try:
                exit_code = _execute_command(args, service, commands_dict)
            except Exception as e:
                print(f"Error executing command: {e}")
                continue

        except KeyboardInterrupt:
            # Handle Ctrl+C
            print("\nSession interrupted. Type 'exit' to quit.")
            continue


def main():
    """Main entry point for CLI application."""
    # Check if running in interactive mode (no arguments)
    if len(sys.argv) == 1:
        # Interactive mode - create single shared service instance
        repo = InMemoryTaskRepository()
        service = TaskService(repo)
        _, commands_dict = _create_parser()
        _start_interactive_session(service, commands_dict)
    else:
        # Non-interactive mode - existing behavior
        repo = InMemoryTaskRepository()
        service = TaskService(repo)
        parser, commands_dict = _create_parser()
        args = parser.parse_args()
        exit_code = _execute_command(args, service, commands_dict)
        sys.exit(exit_code)


if __name__ == "__main__":
    main()
