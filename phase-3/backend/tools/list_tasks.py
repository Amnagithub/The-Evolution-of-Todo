"""list_tasks MCP tool implementation.

Lists tasks for the authenticated user with optional status filter.
"""

from typing import Literal, Optional

from sqlmodel import select

from models import Task
from .base import (
    ToolContext,
    ToolResponse,
    create_error_response,
    create_success_response,
)


def list_tasks(
    context: ToolContext,
    status: Literal["all", "pending", "completed"] = "all",
) -> ToolResponse:
    """List user's tasks with optional status filter.

    Args:
        context: Tool context with user_id and session
        status: Filter by task status ("all", "pending", "completed")

    Returns:
        ToolResponse with list of tasks on success
        ToolResponse with error code and message on failure

    Error codes:
        - invalid_status: Status is not one of the valid options
    """
    # Validate status
    valid_statuses = ("all", "pending", "completed")
    if status not in valid_statuses:
        return create_error_response("invalid_status")

    # Build query
    query = select(Task).where(Task.user_id == context.user_id)

    # Apply status filter
    if status == "pending":
        query = query.where(Task.completed == False)
    elif status == "completed":
        query = query.where(Task.completed == True)

    # Order by creation time (newest first)
    query = query.order_by(Task.created_at.desc())

    # Execute query
    tasks = context.session.exec(query).all()

    # Format results
    task_list = [
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "priority": task.priority,
            "created_at": task.created_at.isoformat() if task.created_at else None,
        }
        for task in tasks
    ]

    return create_success_response({
        "tasks": task_list,
        "count": len(task_list),
    })


async def list_tasks_handler(
    args: dict,
    context: ToolContext,
) -> ToolResponse:
    """Async handler for list_tasks tool (used by AgentRunner).

    Args:
        args: Tool arguments from OpenAI {"status"?: str}
        context: Tool context with user_id and session

    Returns:
        ToolResponse from list_tasks
    """
    return list_tasks(
        status=args.get("status", "all"),
        context=context,
    )
