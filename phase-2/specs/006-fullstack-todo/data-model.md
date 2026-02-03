# Data Model: Phase II - Full-Stack Todo Web Application

**Feature**: 006-fullstack-todo
**Date**: 2026-01-15
**Status**: Complete

## Overview

This document defines the data entities, relationships, and validation rules for the Phase II full-stack todo application.

---

## Entities

### 1. User (Managed by Better Auth)

Better Auth manages user authentication and storage. The backend receives only the `user_id` from JWT tokens.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | string (UUID) | PK, unique | User identifier |
| email | string | unique, required | User email address |
| password_hash | string | required | Bcrypt hash (Better Auth managed) |
| created_at | timestamp | auto | Account creation time |
| updated_at | timestamp | auto | Last update time |

**Notes**:
- User table is created and managed by Better Auth
- Backend only references `user_id` from JWT payload
- No direct user table manipulation in backend code

---

### 2. Task

Core entity for todo items, owned by authenticated users.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | integer | PK, auto-increment | Task identifier |
| title | string(200) | required, 1-200 chars | Task title |
| description | text | optional | Task description |
| completed | boolean | default: false | Completion status |
| user_id | string | FK → User.id, indexed, required | Owner reference |
| created_at | timestamp | auto, default: now | Creation time |
| updated_at | timestamp | auto, on update | Last modification |

**Indexes**:
- `idx_tasks_user_id` on `user_id` (for filtering by owner)
- `idx_tasks_user_created` on `(user_id, created_at DESC)` (for sorted listing)

---

## SQLModel Definitions

### Task Model (Database Table)

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(min_length=1, max_length=200, nullable=False)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    user_id: str = Field(index=True, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### Request/Response Schemas

```python
class TaskCreate(SQLModel):
    """Schema for creating a new task"""
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = None

class TaskUpdate(SQLModel):
    """Schema for updating an existing task (partial)"""
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = None

class TaskToggle(SQLModel):
    """Schema for toggling task completion"""
    completed: bool

class TaskResponse(SQLModel):
    """Schema for task response"""
    id: int
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime
    # Note: user_id not exposed in response
```

---

## Entity Relationships

```
┌─────────────┐         ┌─────────────┐
│    User     │ 1     * │    Task     │
│─────────────│─────────│─────────────│
│ id (PK)     │         │ id (PK)     │
│ email       │         │ title       │
│ password    │         │ description │
│ created_at  │         │ completed   │
│ updated_at  │         │ user_id (FK)│
└─────────────┘         │ created_at  │
                        │ updated_at  │
                        └─────────────┘
```

**Relationship Rules**:
- One User can have many Tasks (1:N)
- Each Task belongs to exactly one User
- Deleting a User should cascade delete their Tasks (or prevent deletion)
- Tasks cannot exist without a valid user_id

---

## Validation Rules

### Task Title
- **Required**: Cannot be null or empty
- **Length**: 1-200 characters
- **Whitespace**: Must contain at least one non-whitespace character
- **Characters**: Any UTF-8 characters allowed

### Task Description
- **Optional**: Can be null
- **Length**: No hard limit (text field)

### Task Completed
- **Required**: Boolean field
- **Default**: false on creation
- **Toggle**: PATCH endpoint flips current value

### User ID
- **Required**: Must be present (from JWT)
- **Format**: String (UUID from Better Auth)
- **Validation**: Verified via JWT middleware (not user input)

---

## State Transitions

### Task Lifecycle

```
┌──────────────┐
│   Created    │
│ (completed   │
│   = false)   │
└──────┬───────┘
       │
       ▼
┌──────────────┐     PATCH /complete
│   Pending    │◄────────────────────┐
│              │                     │
└──────┬───────┘                     │
       │ PATCH /complete             │
       ▼                             │
┌──────────────┐                     │
│  Completed   │─────────────────────┘
│              │
└──────┬───────┘
       │ DELETE
       ▼
┌──────────────┐
│   Deleted    │
│  (removed)   │
└──────────────┘
```

**Allowed Transitions**:
- Created → Pending (implicit on creation)
- Pending ↔ Completed (toggle via PATCH)
- Any state → Deleted (permanent removal)

---

## Database Schema (SQL)

```sql
-- Tasks table (User table managed by Better Auth)
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL CHECK (length(trim(title)) > 0),
    description TEXT,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    user_id VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    -- Foreign key to Better Auth user table
    CONSTRAINT fk_tasks_user FOREIGN KEY (user_id)
        REFERENCES "user"(id) ON DELETE CASCADE
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_tasks_user_id ON tasks(user_id);
CREATE INDEX IF NOT EXISTS idx_tasks_user_created ON tasks(user_id, created_at DESC);
```

---

## Migration Strategy

For MVP, using SQLModel's `create_all()`:

```python
from sqlmodel import SQLModel, create_engine

def init_db(database_url: str):
    engine = create_engine(database_url)
    SQLModel.metadata.create_all(engine)
```

**Notes**:
- Better Auth creates its own tables (user, session, etc.)
- Our tasks table references Better Auth's user table
- For production, consider Alembic migrations
