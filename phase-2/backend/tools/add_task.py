"""add_task MCP tool implementation.

Creates a new task for the authenticated user.
"""

from typing import Optional

from models import Task
from .base import (
    ToolContext,
    ToolResponse,
    create_error_response,
    create_success_response,
)


def add_task(
    title: str,
    context: ToolContext,
    description: Optional[str] = None,
    priority: Optional[str] = "medium",
) -> ToolResponse:
    """Create a new task for the user.

    Args:
        title: Task title (1-255 characters, required)
        context: Tool context with user_id and session
        description: Optional task description
        priority: Task priority (low, medium, high) - defaults to medium

    Returns:
        ToolResponse with task_id, status, title, and priority on success
        ToolResponse with error code and message on failure

    Error codes:
        - empty_title: Title is empty or whitespace-only
        - title_too_long: Title exceeds 255 characters
        - invalid_priority: Priority is not low, medium, or high
    """
    # Validate title
    cleaned_title = title.strip() if title else ""

    if not cleaned_title:
        return create_error_response("empty_title")

    if len(cleaned_title) > 255:
        return create_error_response("title_too_long")

    # Validate and normalize priority
    valid_priorities = ["low", "medium", "high"]
    cleaned_priority = (priority or "medium").lower().strip()
    if cleaned_priority not in valid_priorities:
        cleaned_priority = "medium"

    # Create task
    task = Task(
        user_id=context.user_id,
        title=cleaned_title,
        description=description.strip() if description else None,
        completed=False,
        priority=cleaned_priority,
    )

    # Save to database
    context.session.add(task)
    context.session.commit()
    context.session.refresh(task)

    return create_success_response({
        "task_id": task.id,
        "status": "created",
        "title": task.title,
        "priority": task.priority,
    })


async def add_task_handler(
    args: dict,
    context: ToolContext,
) -> ToolResponse:
    """Async handler for add_task tool (used by AgentRunner).

    Args:
        args: Tool arguments from OpenAI {"title": str, "description"?: str, "priority"?: str}
        context: Tool context with user_id and session

    Returns:
        ToolResponse from add_task
    """
    return add_task(
        title=args.get("title", ""),
        description=args.get("description"),
        priority=args.get("priority", "medium"),
        context=context,
    )
