"""get_user_details MCP tool implementation.

Returns non-sensitive user profile information.
NEVER returns passwords, tokens, recovery codes, or other sensitive data.
"""

from sqlalchemy import text

from .base import (
    ToolContext,
    ToolResponse,
    create_error_response,
    create_success_response,
)


def get_user_details(
    context: ToolContext,
) -> ToolResponse:
    """Get non-sensitive user profile information.

    Args:
        context: Tool context with user_id and session

    Returns:
        ToolResponse with user_id, username, and created_at on success
        ToolResponse with error code and message on failure

    Error codes:
        - unauthorized: User not found (shouldn't happen with valid session)
        - session_expired: Session is no longer valid

    Security:
        - ONLY returns: user_id, username (or name), created_at
        - NEVER returns: password, email, tokens, recovery codes
    """
    # Query the user table for basic info only
    # Better Auth uses a "user" table with various fields
    # We only want to expose: id, name (or username), createdAt
    result = context.session.execute(
        text("""
            SELECT id, name, "createdAt"
            FROM "user"
            WHERE id = :user_id
        """),
        {"user_id": context.user_id}
    ).first()

    if not result:
        # User not found - session might be expired or invalid
        return create_error_response("session_expired")

    user_id, name, created_at = result

    return create_success_response({
        "user_id": user_id,
        "username": name or "Unknown",
        "created_at": created_at.isoformat() if created_at else None,
    })


async def get_user_details_handler(
    args: dict,
    context: ToolContext,
) -> ToolResponse:
    """Async handler for get_user_details tool (used by AgentRunner).

    Args:
        args: Tool arguments from OpenAI (none required)
        context: Tool context with user_id and session

    Returns:
        ToolResponse from get_user_details
    """
    return get_user_details(context=context)
