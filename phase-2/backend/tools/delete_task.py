"""delete_task MCP tool implementation.

Deletes a task permanently for the authenticated user.
"""

from sqlmodel import select

from models import Task
from .base import (
    ToolContext,
    ToolResponse,
    create_error_response,
    create_success_response,
)


def delete_task(
    task_id: int,
    context: ToolContext,
) -> ToolResponse:
    """Delete a task permanently.

    Args:
        task_id: ID of the task to delete
        context: Tool context with user_id and session

    Returns:
        ToolResponse with task_id, status, and title on success
        ToolResponse with error code and message on failure

    Error codes:
        - not_found: Task doesn't exist or doesn't belong to user
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

    # Store title before deletion
    title = task.title

    # Delete the task
    context.session.delete(task)
    context.session.commit()

    return create_success_response({
        "task_id": task_id,
        "status": "deleted",
        "title": title,
    })


async def delete_task_handler(
    args: dict,
    context: ToolContext,
) -> ToolResponse:
    """Async handler for delete_task tool (used by AgentRunner).

    Args:
        args: Tool arguments from OpenAI {"task_id": int}
        context: Tool context with user_id and session

    Returns:
        ToolResponse from delete_task
    """
    task_id = args.get("task_id")
    if task_id is None:
        return create_error_response("not_found", identifier="unknown")

    return delete_task(
        task_id=task_id,
        context=context,
    )
