"""AI Agent module for Todo Chatbot.

This package contains the OpenAI Agent configuration and runner:
- todo_agent: Agent with MCP tools and system instructions
- runner: Agent execution utility with error handling
"""

from .todo_agent import todo_agent, TodoAgent, SYSTEM_INSTRUCTIONS, TOOL_DEFINITIONS
from .runner import agent_runner, AgentRunner

__all__ = [
    "todo_agent",
    "TodoAgent",
    "SYSTEM_INSTRUCTIONS",
    "TOOL_DEFINITIONS",
    "agent_runner",
    "AgentRunner",
]
