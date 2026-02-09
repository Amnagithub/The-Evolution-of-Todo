"""OpenAI Agent for Todo Chatbot.

Configures the AI agent with:
- System instructions for natural language understanding
- MCP tool definitions for task management
- Intent recognition patterns
- Chaining rules for name-based lookups
"""

import os
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")  # For OpenRouter compatibility
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "openai/gpt-4o-mini")

# System instructions for the AI agent
SYSTEM_INSTRUCTIONS = """You are a helpful todo assistant. You help users manage their tasks through natural language commands.

## Available Tools

You have access to the following tools to manage tasks:

1. **add_task**: Create a new task
   - Use when: user says "add", "create", "remember to", "I need to", "don't forget"
   - Required: title (extract from user message)
   - Optional: description, priority (low, medium, high - default: medium)
   - Priority keywords: "urgent"/"important"/"asap" → high, "low priority"/"whenever" → low

2. **list_tasks**: Show user's tasks
   - Use when: user says "show", "list", "what's pending", "all tasks", "my tasks"
   - Optional: status filter ("all", "pending", "completed")

3. **complete_task**: Mark a task as done
   - Use when: user says "done", "complete", "mark as done", "check off", "finished"
   - Required: task_id (use list_tasks first if user provides name instead of ID)

4. **delete_task**: Remove a task permanently
   - Use when: user says "delete", "remove", "cancel", "get rid of"
   - Required: task_id (use list_tasks first if user provides name instead of ID)

5. **update_task**: Change a task's title or description
   - Use when: user says "change", "update", "edit", "rename"
   - Required: task_id, at least one of title or description

6. **get_user_details**: Get user's profile info
   - Use when: user asks "who am I?", "my profile", "user id", "account info"
   - Returns: username and created_at only (never passwords or tokens)

## Chaining Rules

When a user refers to a task by name instead of ID:
1. First call list_tasks to get all tasks
2. Find the best match using fuzzy matching
3. If exactly one match: proceed with the requested operation
4. If multiple matches: ask user to clarify which task they mean
5. If no match: tell user the task wasn't found and offer to list tasks

## Response Guidelines

- Be concise but friendly
- Confirm actions with the task title and ID
- Use checkmarks (✓) for success confirmations
- If something goes wrong, explain what happened
- Never expose internal errors to users
- Never share passwords, tokens, or sensitive user data

## Examples

User: "add buy groceries"
→ Call add_task with title "buy groceries", priority "medium"
→ Respond: "Added 'buy groceries' (ID: 1, priority: medium) ✓"

User: "add urgent meeting with boss"
→ Call add_task with title "meeting with boss", priority "high"
→ Respond: "Added 'meeting with boss' (ID: 2, priority: high) ✓"

User: "show my tasks"
→ Call list_tasks
→ Respond: "Here are your tasks: [formatted list]"

User: "done buy groceries"
→ Call list_tasks to find matching task
→ Call complete_task with the matched task_id
→ Respond: "Marked 'buy groceries' as complete ✓"

User: "who am I?"
→ Call get_user_details
→ Respond: "You're [username], member since [date]"
"""

# Tool definitions for OpenAI function calling
TOOL_DEFINITIONS: List[Dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Create a new task for the user with optional priority",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Task title (1-255 characters)",
                    },
                    "description": {
                        "type": "string",
                        "description": "Optional task description",
                    },
                    "priority": {
                        "type": "string",
                        "enum": ["low", "medium", "high"],
                        "description": "Task priority level (default: medium)",
                        "default": "medium",
                    },
                },
                "required": ["title"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "List user's tasks with optional status filter",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": ["all", "pending", "completed"],
                        "description": "Filter by task status",
                        "default": "all",
                    },
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "complete_task",
            "description": "Mark a task as completed",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "integer",
                        "description": "ID of the task to complete",
                    },
                },
                "required": ["task_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "Delete a task permanently",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "integer",
                        "description": "ID of the task to delete",
                    },
                },
                "required": ["task_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "update_task",
            "description": "Update a task's title or description",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "integer",
                        "description": "ID of the task to update",
                    },
                    "title": {
                        "type": "string",
                        "description": "New title (1-255 characters)",
                    },
                    "description": {
                        "type": "string",
                        "description": "New description",
                    },
                },
                "required": ["task_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_user_details",
            "description": "Get non-sensitive user profile information",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
]


class TodoAgent:
    """OpenAI-powered todo management agent.

    Handles natural language understanding and tool orchestration.
    """

    def __init__(self):
        """Initialize the agent with OpenAI configuration."""
        self.model = OPENAI_MODEL
        self.system_prompt = SYSTEM_INSTRUCTIONS
        self.tools = TOOL_DEFINITIONS
        self.temperature = 0.3  # Low temperature for consistent tool calling

    def get_chat_config(self) -> Dict[str, Any]:
        """Get configuration for OpenAI chat completion.

        Returns:
            Dict with model, messages, tools, and other settings
        """
        return {
            "model": self.model,
            "temperature": self.temperature,
            "tools": self.tools,
            "tool_choice": "auto",
        }

    def build_messages(
        self,
        conversation_history: List[Dict[str, str]],
        user_message: str,
    ) -> List[Dict[str, str]]:
        """Build the messages array for chat completion.

        Args:
            conversation_history: Previous messages in the conversation
            user_message: The current user message

        Returns:
            List of message dicts for OpenAI API
        """
        messages = [
            {"role": "system", "content": self.system_prompt},
        ]

        # Add conversation history
        for msg in conversation_history:
            messages.append({
                "role": msg["role"],
                "content": msg["content"],
            })

        # Add current user message
        messages.append({
            "role": "user",
            "content": user_message,
        })

        return messages


# Singleton instance
todo_agent = TodoAgent()
