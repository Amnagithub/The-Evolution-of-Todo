"""Message model for AI chatbot persistence.

Individual chat messages (user or assistant) with optional tool call data.
"""

from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from sqlmodel import Column, Field, Relationship, SQLModel
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import JSON


if TYPE_CHECKING:
    from .conversation import Conversation


class Message(SQLModel, table=True):
    """Individual chat message (user or assistant).

    Messages cascade delete with their parent conversation.
    """

    __tablename__ = "message"

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(
        foreign_key="conversation.id",
        index=True,
        nullable=False,
        description="Parent conversation ID"
    )
    role: str = Field(
        nullable=False,
        description="Message sender: 'user' or 'assistant'"
    )
    content: str = Field(
        nullable=False,
        description="Message text content"
    )
    tool_calls: Optional[List[Dict[str, Any]]] = Field(
        default=None,
        sa_column=Column(JSON, nullable=True),
        description="Tool invocation data (assistant messages only)"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Message creation time"
    )

    # Relationship to conversation
    conversation: Optional["Conversation"] = Relationship(back_populates="messages")

    @property
    def is_user(self) -> bool:
        """Check if this is a user message."""
        return self.role == "user"

    @property
    def is_assistant(self) -> bool:
        """Check if this is an assistant message."""
        return self.role == "assistant"
