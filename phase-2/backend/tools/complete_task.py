"""complete_task MCP tool implementation.

Marks a task as completed for the authenticated user.
"""

from datetime import datetime

from sqlmodel import select

from models import Task
from .base import (
    ToolContext,
    ToolResponse,
    create_error_response,
    create_success_response,
)


def complete_task(
    task_id: int,
    context: ToolContext,
) -> ToolResponse:
    """Mark a task as completed.

    Args:
        task_id: ID of the task to complete
        context: Tool context with user_id and session

    Returns:
        ToolResponse with task_id, status, and title on success
        ToolResponse with error code and message on failure

    Error codes:
        - not_found: Task doesn't exist or doesn't belong to user
        - already_completed: Task is already marked as done
    """
    # Find the task
    task = context.session.exec(
        select(Task).where(
            Task.id == task_id,
            Task.user_id == context.user_id
        )
    ).first()

    if not task:
        return create_error_response("not_found", identifier=str(task_id))

    # Check if already completed
    if task.completed:
        return create_error_response("already_completed")

    # Mark as completed
    task.completed = True
    task.updated_at = datetime.utcnow()

    context.session.add(task)
    context.session.commit()
    context.session.refresh(task)

    return create_success_response({
        "task_id": task.id,
        "status": "completed",
        "title": task.title,
    })


async def complete_task_handler(
    args: dict,
    context: ToolContext,
) -> ToolResponse:
    """Async handler for complete_task tool (used by AgentRunner).

    Args:
        args: Tool arguments from OpenAI {"task_id": int}
        context: Tool context with user_id and session

    Returns:
        ToolResponse from complete_task
    """
    task_id = args.get("task_id")
    if task_id is None:
        return create_error_response("not_found", identifier="unknown")

    return complete_task(
        task_id=task_id,
        context=context,
    )
