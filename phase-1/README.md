# Phase 1: CLI Todo Application

**Status**: Implemented
**Technology**: Python 3.x, argparse, in-memory/file storage

## Overview

Phase 1 delivers a command-line todo application with task persistence within a terminal session.

## Features

- Add tasks with title and optional description
- List tasks in table, simple, or JSON format
- Filter tasks by status (all, pending, completed)
- Mark tasks as complete/incomplete (reopen)
- Update task title and description
- Delete tasks
- Context-sensitive help

## Architecture

```
src/todo/
├── cli/
│   ├── commands/          # CLI command implementations
│   │   ├── add.py
│   │   ├── list.py
│   │   ├── complete.py
│   │   ├── incomplete.py
│   │   ├── update.py
│   │   ├── delete.py
│   │   └── help.py
│   ├── formatters/        # Output formatting
│   │   ├── table.py
│   │   ├── simple.py
│   │   ├── json_fmt.py
│   │   └── base.py
│   ├── main.py           # CLI entry point
│   └── errors.py         # CLI-specific errors
├── domain/               # Domain models
│   ├── entities.py       # Task entity
│   ├── value_objects.py  # TaskStatus
│   ├── errors.py         # Domain errors
│   ├── repository.py     # In-memory repository
│   ├── file_repository.py # File-based repository
│   └── session_storage.py # JSON file storage
└── services/             # Business logic
    └── task_service.py   # Task operations service
```

## Quick Start

```bash
# Install
pip install -e .

# Add a task
todo add "Buy groceries" "Milk and bread"

# List tasks
todo list
todo list --status pending
todo list --format simple

# Complete a task
todo complete 1

# Reopen a task
todo reopen 1
todo incomplete 1

# Update a task
todo update 1 --title "New title" --desc "New description"

# Delete a task
todo delete 1

# Get help
todo help
todo help add
```

## Storage

Tasks are persisted to `.todo/tasks.json` within the current working directory. Each terminal session maintains its own storage file.

## Specifications

- [Todo Domain Model](./specs/todo-domain.md)
- [CLI Interface](./specs/cli-interface.md)
- [CLI State Scope](./specs/cli-state-scope.md)

## Test Results

All 59 tests pass:
- Unit tests for commands (add, list, complete, incomplete, update, delete, help)
- Unit tests for formatters (table, simple, JSON)
- Integration tests for workflow operations

  ## Demo

[Watch the demo video](https://www.loom.com/share/306bdec1e3bd4b0b8f0ac0d7480ab142)

## Future Phases

- **Phase 2**: Web + Database (Flask/FastAPI, SQLite)
- **Phase 3**: AI Chatbot (LLM integration)
- **Phase 4**: Local Kubernetes (Docker, K8s)
- **Phase 5**: Cloud-native (AWS/GCP, event streaming)
