"""MCP Tools for AI Todo Chatbot.

This package contains all MCP tool implementations for the AI chatbot:
- add_task: Create new tasks
- list_tasks: List tasks with optional filters
- complete_task: Mark tasks as completed
- delete_task: Delete tasks permanently
- update_task: Update task title/description
- get_user_details: Get non-sensitive user profile info
"""

from .base import (
    ToolContext,
    ToolResponse,
    create_error_response,
    create_success_response,
    fuzzy_match_task,
    find_task_by_id_or_name,
)
from .add_task import add_task, add_task_handler
from .list_tasks import list_tasks, list_tasks_handler
from .complete_task import complete_task, complete_task_handler
from .delete_task import delete_task, delete_task_handler
from .update_task import update_task, update_task_handler
from .get_user_details import get_user_details, get_user_details_handler
from .schemas import (
    AddTaskArgs,
    ListTasksArgs,
    CompleteTaskArgs,
    DeleteTaskArgs,
    UpdateTaskArgs,
    GetUserDetailsArgs,
    TaskResult,
    TaskItem,
    TaskListResult,
    UserDetailsResult,
    ToolError,
    ToolCallRecord,
    ChatRequest,
    ChatResponse,
    MessageItem,
    ChatHistoryResponse,
)

__all__ = [
    # Base utilities
    "ToolContext",
    "ToolResponse",
    "create_error_response",
    "create_success_response",
    "fuzzy_match_task",
    "find_task_by_id_or_name",
    # Tool implementations
    "add_task",
    "add_task_handler",
    "list_tasks",
    "list_tasks_handler",
    "complete_task",
    "complete_task_handler",
    "delete_task",
    "delete_task_handler",
    "update_task",
    "update_task_handler",
    "get_user_details",
    "get_user_details_handler",
    # Argument schemas
    "AddTaskArgs",
    "ListTasksArgs",
    "CompleteTaskArgs",
    "DeleteTaskArgs",
    "UpdateTaskArgs",
    "GetUserDetailsArgs",
    # Result schemas
    "TaskResult",
    "TaskItem",
    "TaskListResult",
    "UserDetailsResult",
    "ToolError",
    "ToolCallRecord",
    # Chat schemas
    "ChatRequest",
    "ChatResponse",
    "MessageItem",
    "ChatHistoryResponse",
]
