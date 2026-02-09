"""Base classes and utilities for MCP tools.

Provides ToolContext for passing authenticated user info to tools,
and base classes for consistent tool implementation.
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from difflib import SequenceMatcher

from sqlmodel import Session

from models import Task


@dataclass
class ToolContext:
    """Context passed to all MCP tools.

    Contains authenticated user info and database session.
    Tools should never trust user_id from arguments - always use context.
    """

    user_id: str
    session: Session

    def validate_ownership(self, resource_user_id: str) -> bool:
        """Validate that the authenticated user owns the resource."""
        return self.user_id == resource_user_id


@dataclass
class ToolResponse:
    """Standard response format for all tools.

    Either success=True with data, or success=False with error info.
    """

    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    message: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        if self.success:
            return self.data or {}
        return {
            "error": self.error or "unknown_error",
            "message": self.message or "An unexpected error occurred"
        }


# Error response templates from spec
ERROR_TEMPLATES = {
    "unauthorized": "You can only manage your own data",
    "not_found": "I couldn't find a task matching '{identifier}'. Want me to list your current tasks?",
    "empty_title": "Please give me a valid title (max 255 chars for title).",
    "title_too_long": "Please give me a valid title (max 255 chars for title).",
    "already_completed": "This task is already marked as done.",
    "no_changes": "Looks like nothing changed — did you want to update something?",
    "invalid_status": "Status must be 'all', 'pending', or 'completed'.",
    "session_expired": "Your session has expired. Please sign in again.",
}


def create_error_response(error_code: str, **kwargs) -> ToolResponse:
    """Create a standardized error response.

    Args:
        error_code: Key from ERROR_TEMPLATES
        **kwargs: Format arguments for the message template

    Returns:
        ToolResponse with success=False
    """
    template = ERROR_TEMPLATES.get(error_code, "An unexpected error occurred")
    message = template.format(**kwargs) if kwargs else template
    return ToolResponse(success=False, error=error_code, message=message)


def create_success_response(data: Dict[str, Any]) -> ToolResponse:
    """Create a standardized success response.

    Args:
        data: Response data to include

    Returns:
        ToolResponse with success=True
    """
    return ToolResponse(success=True, data=data)


def fuzzy_match_task(
    query: str,
    tasks: List[Task],
    threshold: float = 0.6
) -> List[Task]:
    """Find tasks matching a query string using fuzzy matching.

    Args:
        query: Search string (task title or partial match)
        tasks: List of tasks to search
        threshold: Minimum similarity ratio (0.0-1.0), default 0.6

    Returns:
        List of matching tasks, sorted by similarity (best match first)
    """
    query_lower = query.lower().strip()
    matches = []

    for task in tasks:
        title_lower = task.title.lower()

        # Exact match
        if query_lower == title_lower:
            matches.append((task, 1.0))
            continue

        # Contains match (high confidence)
        if query_lower in title_lower or title_lower in query_lower:
            # Calculate a score based on how much of the title is matched
            score = len(query_lower) / len(title_lower)
            matches.append((task, max(score, 0.8)))
            continue

        # Fuzzy match using SequenceMatcher
        ratio = SequenceMatcher(None, query_lower, title_lower).ratio()
        if ratio >= threshold:
            matches.append((task, ratio))

    # Sort by similarity score (highest first)
    matches.sort(key=lambda x: x[1], reverse=True)
    return [task for task, _ in matches]


def find_task_by_id_or_name(
    identifier: str,
    context: ToolContext
) -> tuple[Optional[Task], List[Task]]:
    """Find a task by ID or name with fuzzy matching.

    Args:
        identifier: Task ID (integer) or name (string)
        context: Tool context with session and user_id

    Returns:
        Tuple of (exact_match, fuzzy_matches)
        - If ID lookup: (task, []) or (None, [])
        - If name lookup: (task, []) if unique match, (None, matches) if multiple
    """
    from sqlmodel import select

    # Try to parse as integer ID
    try:
        task_id = int(identifier)
        task = context.session.exec(
            select(Task).where(
                Task.id == task_id,
                Task.user_id == context.user_id
            )
        ).first()
        return (task, [])
    except ValueError:
        pass

    # Name-based lookup with fuzzy matching
    all_tasks = context.session.exec(
        select(Task).where(Task.user_id == context.user_id)
    ).all()

    matches = fuzzy_match_task(identifier, list(all_tasks))

    if len(matches) == 1:
        return (matches[0], [])
    elif len(matches) > 1:
        return (None, matches)
    else:
        return (None, [])
