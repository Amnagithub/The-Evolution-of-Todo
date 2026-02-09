"""Agent runner utility for executing AI responses.

Handles:
- OpenAI API calls with error handling
- Tool execution orchestration
- Response parsing and formatting
- Exponential backoff for rate limits
"""

import json
import time
from typing import Any, Callable, Dict, List, Optional, Tuple

from openai import OpenAI, RateLimitError, APIError

from .todo_agent import todo_agent, OPENAI_API_KEY, OPENAI_BASE_URL
from tools import (
    ToolContext,
    ToolResponse,
    add_task_handler,
    list_tasks_handler,
    complete_task_handler,
    delete_task_handler,
    update_task_handler,
    get_user_details_handler,
)
from tools.schemas import ToolCallRecord


# Maximum retries for rate-limited requests
MAX_RETRIES = 3
BASE_DELAY = 1.0  # seconds

# Default tool handlers - all 6 MCP tools
DEFAULT_TOOL_HANDLERS = {
    "add_task": add_task_handler,
    "list_tasks": list_tasks_handler,
    "complete_task": complete_task_handler,
    "delete_task": delete_task_handler,
    "update_task": update_task_handler,
    "get_user_details": get_user_details_handler,
}


class AgentRunner:
    """Executes agent responses with tool orchestration.

    Handles the complete flow from user message to final response,
    including any tool calls that need to be made.
    """

    def __init__(self, tool_handlers: Optional[Dict[str, Callable]] = None):
        """Initialize the runner.

        Args:
            tool_handlers: Dict mapping tool names to handler functions.
                           Each handler takes (args: dict, context: ToolContext) -> ToolResponse
        """
        # Initialize OpenAI client with optional base_url for OpenRouter compatibility
        if OPENAI_API_KEY:
            client_kwargs = {"api_key": OPENAI_API_KEY}
            if OPENAI_BASE_URL:
                client_kwargs["base_url"] = OPENAI_BASE_URL
            self.client = OpenAI(**client_kwargs)
        else:
            self.client = None
        # Use provided handlers or default handlers
        self.tool_handlers = tool_handlers if tool_handlers is not None else DEFAULT_TOOL_HANDLERS.copy()

    def register_tool(self, name: str, handler: Callable) -> None:
        """Register a tool handler.

        Args:
            name: Tool name (must match TOOL_DEFINITIONS)
            handler: Function (args, context) -> ToolResponse
        """
        self.tool_handlers[name] = handler

    async def run(
        self,
        user_message: str,
        conversation_history: List[Dict[str, str]],
        context: ToolContext,
    ) -> Tuple[str, List[ToolCallRecord]]:
        """Process a user message and return the assistant response.

        Args:
            user_message: The user's input
            conversation_history: Previous messages for context
            context: Tool context with user_id and session

        Returns:
            Tuple of (assistant_response, list of tool calls made)

        Raises:
            ValueError: If OpenAI API key is not configured
            RuntimeError: If API call fails after retries
        """
        if not self.client:
            raise ValueError("OpenAI API key not configured")

        # Build messages
        messages = todo_agent.build_messages(conversation_history, user_message)
        config = todo_agent.get_chat_config()

        # Track tool calls for response
        tool_calls_made: List[ToolCallRecord] = []

        # Call OpenAI with retry logic
        response = await self._call_with_retry(
            messages=messages,
            **config,
        )

        # Process response and handle tool calls
        assistant_message = response.choices[0].message

        # If no tool calls, return the response directly
        if not assistant_message.tool_calls:
            return assistant_message.content or "", tool_calls_made

        # Handle tool calls
        messages.append(assistant_message.model_dump())

        for tool_call in assistant_message.tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)

            # Execute tool
            result = await self._execute_tool(tool_name, tool_args, context)

            # Record the tool call
            tool_calls_made.append(ToolCallRecord(
                tool=tool_name,
                arguments=tool_args,
                result=result.to_dict(),
            ))

            # Add tool result to messages
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result.to_dict()),
            })

        # Get final response after tool calls
        final_response = await self._call_with_retry(
            messages=messages,
            **{k: v for k, v in config.items() if k != "tools"},  # No tools for final response
        )

        final_content = final_response.choices[0].message.content or ""
        return final_content, tool_calls_made

    async def _call_with_retry(self, **kwargs) -> Any:
        """Call OpenAI API with exponential backoff retry.

        Args:
            **kwargs: Arguments for chat.completions.create

        Returns:
            OpenAI ChatCompletion response

        Raises:
            RuntimeError: If all retries are exhausted
        """
        last_error = None

        for attempt in range(MAX_RETRIES):
            try:
                return self.client.chat.completions.create(**kwargs)
            except RateLimitError as e:
                last_error = e
                delay = BASE_DELAY * (2 ** attempt)
                print(f"Rate limited, retrying in {delay}s (attempt {attempt + 1}/{MAX_RETRIES})")
                time.sleep(delay)
            except APIError as e:
                last_error = e
                if attempt < MAX_RETRIES - 1:
                    delay = BASE_DELAY * (2 ** attempt)
                    print(f"API error, retrying in {delay}s: {e}")
                    time.sleep(delay)
                else:
                    raise

        raise RuntimeError(f"OpenAI API call failed after {MAX_RETRIES} retries: {last_error}")

    async def _execute_tool(
        self,
        tool_name: str,
        args: Dict[str, Any],
        context: ToolContext,
    ) -> ToolResponse:
        """Execute a tool and return the result.

        Args:
            tool_name: Name of the tool to execute
            args: Arguments for the tool
            context: Tool context with user_id and session

        Returns:
            ToolResponse with result or error
        """
        handler = self.tool_handlers.get(tool_name)

        if not handler:
            return ToolResponse(
                success=False,
                error="unknown_tool",
                message=f"Tool '{tool_name}' is not available",
            )

        try:
            return await handler(args, context)
        except Exception as e:
            print(f"Tool execution error ({tool_name}): {e}")
            return ToolResponse(
                success=False,
                error="execution_error",
                message="Sorry, something went wrong while processing your request.",
            )


# Singleton instance
agent_runner = AgentRunner()
