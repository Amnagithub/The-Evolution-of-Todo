"""Pydantic schemas for MCP tool request/response validation.

These schemas define the structure of tool arguments and results
for integration with the OpenAI Agents SDK.
"""

from datetime import datetime
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


# ============================================================================
# Tool Argument Schemas
# ============================================================================

class AddTaskArgs(BaseModel):
    """Arguments for add_task tool."""

    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Task title"
    )
    description: Optional[str] = Field(
        default=None,
        description="Optional task description"
    )


class ListTasksArgs(BaseModel):
    """Arguments for list_tasks tool."""

    status: Literal["all", "pending", "completed"] = Field(
        default="all",
        description="Filter by task status"
    )


class CompleteTaskArgs(BaseModel):
    """Arguments for complete_task tool."""

    task_id: int = Field(..., description="ID of the task to complete")


class DeleteTaskArgs(BaseModel):
    """Arguments for delete_task tool."""

    task_id: int = Field(..., description="ID of the task to delete")


class UpdateTaskArgs(BaseModel):
    """Arguments for update_task tool."""

    task_id: int = Field(..., description="ID of the task to update")
    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=255,
        description="New title"
    )
    description: Optional[str] = Field(
        default=None,
        description="New description"
    )


class GetUserDetailsArgs(BaseModel):
    """Arguments for get_user_details tool (none required)."""
    pass


# ============================================================================
# Tool Result Schemas
# ============================================================================

class TaskResult(BaseModel):
    """Result for task mutation operations (add, complete, delete, update)."""

    task_id: int = Field(..., description="ID of the affected task")
    status: Literal["created", "completed", "deleted", "updated"] = Field(
        ...,
        description="Operation result"
    )
    title: str = Field(..., description="Task title")


class TaskItem(BaseModel):
    """Single task in list results."""

    id: int
    title: str
    description: Optional[str] = None
    completed: bool
    priority: Literal["low", "medium", "high"] = "medium"
    created_at: datetime


class TaskListResult(BaseModel):
    """Result for list_tasks operation."""

    tasks: List[TaskItem]
    count: int


class UserDetailsResult(BaseModel):
    """Result for get_user_details operation."""

    user_id: str = Field(..., description="User identifier")
    username: str = Field(..., description="Display name")
    created_at: datetime = Field(..., description="Account creation date")


class ToolError(BaseModel):
    """Error response from any tool."""

    error: Literal[
        "unauthorized",
        "not_found",
        "validation_error",
        "already_completed",
        "empty_title",
        "title_too_long",
        "no_changes",
        "invalid_status",
        "session_expired"
    ] = Field(..., description="Error code")
    message: str = Field(..., description="Human-friendly error message")


# ============================================================================
# Tool Call Tracking
# ============================================================================

class ToolCallRecord(BaseModel):
    """Record of a tool invocation for persistence."""

    tool: Literal[
        "add_task",
        "list_tasks",
        "complete_task",
        "delete_task",
        "update_task",
        "get_user_details"
    ]
    arguments: Dict[str, Any]
    result: Dict[str, Any]


# ============================================================================
# Chat Message Schemas
# ============================================================================

class ChatRequest(BaseModel):
    """Request body for POST /api/chat."""

    message: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="User's natural language message"
    )


class ChatResponse(BaseModel):
    """Response body for POST /api/chat."""

    message: str = Field(..., description="Assistant's response")
    tool_calls: List[ToolCallRecord] = Field(
        default_factory=list,
        description="Tools invoked during response"
    )
    conversation_id: int = Field(..., description="Conversation ID")


class MessageItem(BaseModel):
    """Single message in history."""

    id: int
    role: Literal["user", "assistant"]
    content: str
    tool_calls: Optional[List[ToolCallRecord]] = None
    created_at: datetime


class ChatHistoryResponse(BaseModel):
    """Response body for GET /api/chat/history."""

    messages: List[MessageItem]
    conversation_id: int
    total_count: int
