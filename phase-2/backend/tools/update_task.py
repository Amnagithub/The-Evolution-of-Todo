"""update_task MCP tool implementation.

Updates a task's title or description for the authenticated user.
"""

from datetime import datetime
from typing import Optional

from sqlmodel import select

from models import Task
from .base import (
    ToolContext,
    ToolResponse,
    create_error_response,
    create_success_response,
)


def update_task(
    task_id: int,
    context: ToolContext,
    title: Optional[str] = None,
    description: Optional[str] = None,
) -> ToolResponse:
    """Update a task's title or description.

    Args:
        task_id: ID of the task to update
        context: Tool context with user_id and session
        title: New title (1-255 characters, optional)
        description: New description (optional)

    Returns:
        ToolResponse with task_id, status, and title on success
        ToolResponse with error code and message on failure

    Error codes:
        - not_found: Task doesn't exist or doesn't belong to user
        - no_changes: Neither title nor description provided
        - empty_title: Title is empty or whitespace-only
        - title_too_long: Title exceeds 255 characters
    """
    # Check if any changes are requested
    if title is None and description is None:
        return create_error_response("no_changes")

    # Validate title if provided
    if title is not None:
        cleaned_title = title.strip()
        if not cleaned_title:
            return create_error_response("empty_title")
        if len(cleaned_title) > 255:
            return create_error_response("title_too_long")

    # Find the task
    task = context.session.exec(
        select(Task).where(
            Task.id == task_id,
            Task.user_id == context.user_id
        )
    ).first()

    if not task:
        return create_error_response("not_found", identifier=str(task_id))

    # Track if any actual changes were made
    changes_made = False

    # Apply updates
    if title is not None:
        cleaned_title = title.strip()
        if cleaned_title != task.title:
            task.title = cleaned_title
            changes_made = True

    if description is not None:
        cleaned_description = description.strip() if description else None
        if cleaned_description != task.description:
            task.description = cleaned_description
            changes_made = True

    # Check if anything actually changed
    if not changes_made:
        return create_error_response("no_changes")

    # Update timestamp
    task.updated_at = datetime.utcnow()

    context.session.add(task)
    context.session.commit()
    context.session.refresh(task)

    return create_success_response({
        "task_id": task.id,
        "status": "updated",
        "title": task.title,
    })


async def update_task_handler(
    args: dict,
    context: ToolContext,
) -> ToolResponse:
    """Async handler for update_task tool (used by AgentRunner).

    Args:
        args: Tool arguments from OpenAI {"task_id": int, "title"?: str, "description"?: str}
        context: Tool context with user_id and session

    Returns:
        ToolResponse from update_task
    """
    task_id = args.get("task_id")
    if task_id is None:
        return create_error_response("not_found", identifier="unknown")

    return update_task(
        task_id=task_id,
        title=args.get("title"),
        description=args.get("description"),
        context=context,
    )
