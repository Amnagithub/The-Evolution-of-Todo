"""
Base command class for CLI commands.
"""

from abc import ABC, abstractmethod
from argparse import ArgumentParser

from todo.services.task_service import TaskService


class Command(ABC):
    """Base class for all CLI commands."""

    @abstractmethod
    def setup_parser(self, parser: ArgumentParser) -> None:
        """Configure argument parser for this command."""
        pass

    @abstractmethod
    def execute(self, args, service: TaskService) -> int:
        """Execute the command.

        Returns:
            Exit code (0 for success, non-zero for error)
        """
        pass
