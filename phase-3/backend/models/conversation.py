"""Conversation model for AI chatbot persistence.

One conversation per user (UNIQUE constraint on user_id).
"""

from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .message import Message


class Conversation(SQLModel, table=True):
    """Groups messages for a chat session.

    Design decision: One conversation per user (simplest approach).
    """

    __tablename__ = "conversation"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(
        index=True,
        unique=True,
        nullable=False,
        description="Owner's user ID (one conversation per user)"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="First message time"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Last activity time"
    )

    # Relationship to messages
    messages: List["Message"] = Relationship(
        back_populates="conversation",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

    def touch(self) -> None:
        """Update the updated_at timestamp."""
        self.updated_at = datetime.utcnow()
