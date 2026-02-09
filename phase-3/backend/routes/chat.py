"""Chat endpoints for AI Todo Chatbot.

Provides:
- POST /api/chat - Send message and get AI response
- GET /api/chat/history - Get conversation history
- DELETE /api/chat/clear - Clear conversation history
"""

import os
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from database import get_session
from middleware.jwt_auth import get_current_user_id
from models import Conversation, Message
from tools import ToolContext
from tools.schemas import (
    ChatRequest,
    ChatResponse,
    ChatHistoryResponse,
    MessageItem,
    ToolCallRecord,
)
from agent import agent_runner

router = APIRouter(prefix="/api/chat", tags=["Chat"])


def get_or_create_conversation(
    user_id: str,
    session: Session
) -> Conversation:
    """Get existing conversation or create new one for user.

    Design: One conversation per user (UNIQUE constraint).
    """
    conversation = session.exec(
        select(Conversation).where(Conversation.user_id == user_id)
    ).first()

    if not conversation:
        conversation = Conversation(user_id=user_id)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)

    return conversation


def get_conversation_history(
    conversation: Conversation,
    session: Session,
    limit: int = 20,
) -> List[dict]:
    """Get recent conversation history for context.

    Args:
        conversation: The user's conversation
        session: Database session
        limit: Maximum messages to include

    Returns:
        List of message dicts with role and content
    """
    messages = session.exec(
        select(Message)
        .where(Message.conversation_id == conversation.id)
        .order_by(Message.created_at.desc())
        .limit(limit)
    ).all()

    # Reverse to get chronological order
    messages = list(reversed(messages))

    return [
        {"role": msg.role, "content": msg.content}
        for msg in messages
    ]


@router.post("", response_model=ChatResponse)
async def send_message(
    request: ChatRequest,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session),
) -> ChatResponse:
    """Send a chat message and receive AI response.

    The AI agent may invoke MCP tools to manage tasks.
    Messages are persisted to the conversation history.
    """
    # Get or create conversation
    conversation = get_or_create_conversation(user_id, session)

    # Save user message
    user_message = Message(
        conversation_id=conversation.id,
        role="user",
        content=request.message,
    )
    session.add(user_message)
    session.commit()

    # Update conversation timestamp
    conversation.updated_at = datetime.utcnow()

    # Check if OpenAI API is configured
    openai_key = os.getenv("OPENAI_API_KEY")

    if not openai_key:
        # Fallback response when OpenAI is not configured
        assistant_content = (
            f"I received your message: '{request.message}'. "
            "AI agent not configured - please set OPENAI_API_KEY."
        )
        tool_calls: List[ToolCallRecord] = []
    else:
        # Get conversation history for context
        history = get_conversation_history(conversation, session)

        # Create tool context
        context = ToolContext(user_id=user_id, session=session)

        try:
            # Run the agent
            assistant_content, tool_calls = await agent_runner.run(
                user_message=request.message,
                conversation_history=history,
                context=context,
            )
        except Exception as e:
            # Handle agent errors gracefully
            print(f"Agent error: {e}")
            assistant_content = (
                "Sorry, I encountered an error processing your request. "
                "Please try again."
            )
            tool_calls = []

    # Save assistant message
    assistant_message = Message(
        conversation_id=conversation.id,
        role="assistant",
        content=assistant_content,
        tool_calls=[tc.model_dump() for tc in tool_calls] if tool_calls else None,
    )
    session.add(assistant_message)
    session.commit()

    return ChatResponse(
        message=assistant_content,
        tool_calls=tool_calls,
        conversation_id=conversation.id,
    )


@router.get("/history", response_model=ChatHistoryResponse)
async def get_history(
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session),
) -> ChatHistoryResponse:
    """Get conversation history for the authenticated user.

    Messages are ordered by creation time (oldest first).
    """
    # Get conversation
    conversation = session.exec(
        select(Conversation).where(Conversation.user_id == user_id)
    ).first()

    if not conversation:
        # No conversation yet, return empty history
        return ChatHistoryResponse(
            messages=[],
            conversation_id=0,
            total_count=0,
        )

    # Get total count
    all_messages = session.exec(
        select(Message).where(Message.conversation_id == conversation.id)
    ).all()
    total_count = len(all_messages)

    # Get paginated messages
    messages = session.exec(
        select(Message)
        .where(Message.conversation_id == conversation.id)
        .order_by(Message.created_at)
        .offset(offset)
        .limit(limit)
    ).all()

    # Convert to response format
    message_items = [
        MessageItem(
            id=msg.id,
            role=msg.role,
            content=msg.content,
            tool_calls=[ToolCallRecord(**tc) for tc in msg.tool_calls] if msg.tool_calls else None,
            created_at=msg.created_at,
        )
        for msg in messages
    ]

    return ChatHistoryResponse(
        messages=message_items,
        conversation_id=conversation.id,
        total_count=total_count,
    )


@router.delete("/clear", status_code=204)
async def clear_history(
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session),
) -> None:
    """Clear all messages in the user's conversation.

    The conversation record is retained but all messages are deleted.
    """
    conversation = session.exec(
        select(Conversation).where(Conversation.user_id == user_id)
    ).first()

    if conversation:
        # Delete all messages (cascade would also work via FK)
        messages = session.exec(
            select(Message).where(Message.conversation_id == conversation.id)
        ).all()
        for msg in messages:
            session.delete(msg)

        # Reset conversation timestamp
        conversation.updated_at = datetime.utcnow()
        session.commit()

    # 204 No Content - success with no response body
    return None
