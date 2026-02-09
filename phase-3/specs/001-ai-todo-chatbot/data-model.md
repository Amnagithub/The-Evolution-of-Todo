# Data Model: AI Todo Chatbot (Phase III)

**Branch**: `001-ai-todo-chatbot`
**Date**: 2026-02-05
**Status**: Complete

---

## Entity Overview

Phase III introduces two new entities for conversation persistence while reusing existing Phase II entities.

```
┌─────────────────────────────────────────────────────────────────────┐
│                           USER (Phase II)                           │
│  Reused from Better Auth - no modifications needed                  │
└─────────────────────────────────────────────────────────────────────┘
        │                                    │
        │ 1:N                                │ 1:N
        ▼                                    ▼
┌───────────────────┐              ┌───────────────────────┐
│   TASK (Phase II) │              │  CONVERSATION (new)   │
│   Extended        │              │  Phase III            │
└───────────────────┘              └───────────────────────┘
                                             │
                                             │ 1:N
                                             ▼
                                   ┌───────────────────────┐
                                   │    MESSAGE (new)      │
                                   │    Phase III          │
                                   └───────────────────────┘
```

---

## Existing Entities (Phase II - No Changes)

### User

**Source**: Better Auth managed table
**Purpose**: Represents authenticated users

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | VARCHAR(255) | PRIMARY KEY | Better Auth generated |
| username | VARCHAR(255) | UNIQUE, NOT NULL | Display name |
| email | VARCHAR(255) | UNIQUE, NOT NULL | Login identifier |
| created_at | TIMESTAMP | NOT NULL | Account creation |
| *[other Better Auth fields]* | - | - | Passwords, tokens, etc. (never exposed) |

**Exposed fields for get_user_details**: id, username, created_at only

### Task

**Source**: `backend/models/task.py` (Phase II)
**Purpose**: Represents user's todo items

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | INTEGER | PRIMARY KEY, AUTO | Unique identifier |
| user_id | VARCHAR(255) | FK(user.id), NOT NULL, INDEX | Ownership |
| title | VARCHAR(255) | NOT NULL, min=1 | Task title |
| description | TEXT | NULLABLE | Optional details |
| completed | BOOLEAN | NOT NULL, DEFAULT=false | Completion status |
| priority | VARCHAR(20) | DEFAULT='medium' | low/medium/high |
| created_at | TIMESTAMP | NOT NULL | Creation time |
| updated_at | TIMESTAMP | NOT NULL | Last modification |

**Validation rules**:
- `title`: 1-255 characters, required
- `priority`: enum of 'low', 'medium', 'high'
- `user_id`: must match authenticated user

---

## New Entities (Phase III)

### Conversation

**Purpose**: Groups messages for a chat session
**Design decision**: One conversation per user (simplest approach)

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | INTEGER | PRIMARY KEY, AUTO | Unique identifier |
| user_id | VARCHAR(255) | FK(user.id), UNIQUE, NOT NULL | Owner (one per user) |
| created_at | TIMESTAMP | NOT NULL, DEFAULT=NOW | First message time |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT=NOW | Last activity time |

**Relationships**:
- `user_id` → `user.id` (Many-to-One)
- `messages` ← `message.conversation_id` (One-to-Many)

**Validation rules**:
- `user_id`: must match authenticated user
- Only one conversation per user (UNIQUE constraint)

**State transitions**:
- Created: When user sends first message
- Updated: `updated_at` refreshed on each new message

### Message

**Purpose**: Individual chat message (user or assistant)

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | INTEGER | PRIMARY KEY, AUTO | Unique identifier |
| conversation_id | INTEGER | FK(conversation.id), NOT NULL | Parent conversation |
| role | VARCHAR(20) | NOT NULL | 'user' or 'assistant' |
| content | TEXT | NOT NULL | Message text |
| tool_calls | JSONB | NULLABLE | Tool invocation data |
| created_at | TIMESTAMP | NOT NULL, DEFAULT=NOW | Message time |

**Relationships**:
- `conversation_id` → `conversation.id` (Many-to-One, CASCADE DELETE)

**Validation rules**:
- `role`: must be 'user' or 'assistant'
- `content`: must not be empty
- `tool_calls`: valid JSON array or null

**tool_calls JSON schema**:
```json
[
  {
    "tool": "add_task",
    "arguments": {"title": "Buy groceries"},
    "result": {"task_id": 1, "status": "created", "title": "Buy groceries"}
  }
]
```

---

## MCP Tool Response Shapes

### add_task

```json
{
  "task_id": 1,
  "status": "created",
  "title": "Buy groceries"
}
```

### list_tasks

```json
[
  {
    "id": 1,
    "title": "Buy groceries",
    "description": null,
    "completed": false,
    "priority": "medium",
    "created_at": "2026-02-05T12:00:00Z"
  }
]
```

### complete_task

```json
{
  "task_id": 1,
  "status": "completed",
  "title": "Buy groceries"
}
```

### delete_task

```json
{
  "task_id": 1,
  "status": "deleted",
  "title": "Buy groceries"
}
```

### update_task

```json
{
  "task_id": 1,
  "status": "updated",
  "title": "Buy almond milk"
}
```

### get_user_details

```json
{
  "user_id": "abc123",
  "username": "john_doe",
  "created_at": "2025-01-15T10:30:00Z"
}
```

---

## Error Response Shape

All tools use consistent error format:

```json
{
  "error": "unauthorized|not_found|validation_error",
  "message": "Human-friendly error message"
}
```

---

## Database Migration

### Alembic Migration Script (outline)

```python
# Migration: Add Phase III chat tables

def upgrade():
    # Create conversation table
    op.create_table(
        'conversation',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id')
    )
    op.create_index('ix_conversation_user_id', 'conversation', ['user_id'])

    # Create message table
    op.create_table(
        'message',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('conversation_id', sa.Integer(), nullable=False),
        sa.Column('role', sa.String(20), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('tool_calls', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversation.id'], ondelete='CASCADE')
    )
    op.create_index('ix_message_conversation_id', 'message', ['conversation_id'])

def downgrade():
    op.drop_table('message')
    op.drop_table('conversation')
```

---

## Index Strategy

| Table | Index | Purpose |
|-------|-------|---------|
| conversation | user_id (UNIQUE) | Fast lookup by user |
| message | conversation_id | Fast message retrieval |
| task | user_id | Already exists in Phase II |

---

## Data Retention

- **Conversations**: Persist indefinitely (user's chat history)
- **Messages**: Cascade delete with conversation
- **Tasks**: Already managed in Phase II (user can delete)

---

## Security Constraints

1. **User isolation**: All queries filter by `user_id` from authenticated session
2. **Sensitive data**: Never expose user.password, user.token, etc.
3. **Tool authorization**: Every tool validates `user_id == authenticated_user.id`
4. **SQL injection**: SQLModel/SQLAlchemy parameterized queries only
