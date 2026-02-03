# Feature Specification: Task Organization

**Feature ID:** 004-task-organization
**Status:** Draft
**Priority:** High
**Created:** 2026-01-02

## 1. Overview

Extend the Todo CLI with organizational features including priority levels, tagging system, search functionality, filtering capabilities, and sorting options to help users manage and locate tasks efficiently.

## 2. User Stories

| ID | As a... | I want to... | So that... |
|----|---------|--------------|------------|
| US-001 | user | assign priority levels to tasks (high/medium/low) | I can focus on what's most important |
| US-002 | user | add multiple tags to a task | I can categorize tasks by context/project |
| US-003 | user | search tasks by keyword | I can quickly find specific tasks |
| US-004 | user | filter tasks by status (completed/incomplete) | I can see only relevant tasks |
| US-005 | user | filter tasks by priority level | I can focus on high-priority items |
| US-006 | user | filter tasks by tag | I can view tasks in a specific category |
| US-007 | user | sort tasks by title (ascending/descending) | I can find tasks alphabetically |
| US-008 | user | sort tasks by priority (high to low / low to high) | I can see most important first |
| US-009 | user | sort tasks by creation order (newest/oldest first) | I can track task chronology |
| US-010 | user | see priority and tags in list output | I can quickly scan task details |

## 3. Domain Model Changes

### 3.1 Extended Task Entity

```python
class Task:
    id: int                    # Unique identifier (auto-incremented)
    title: str                 # Task title/description
    description: str           # Optional detailed description
    status: TaskStatus         # ACTIVE, COMPLETED, ARCHIVED
    priority: Priority         # HIGH, MEDIUM, LOW (default: MEDIUM)
    tags: list[str]            # List of tag labels (default: empty)
    created_at: datetime       # Creation timestamp
    updated_at: datetime       # Last modification timestamp
```

### 3.2 New Enums

```python
from enum import Enum, auto

class Priority(Enum):
    HIGH = auto()
    MEDIUM = auto()
    LOW = auto()

class TaskStatus(Enum):
    ACTIVE = auto()      # Not yet completed
    COMPLETED = auto()   # Finished
    ARCHIVED = auto()    # No longer relevant (future)
```

### 3.3 Task Entity Invariants

1. `id` must be unique and positive integer
2. `title` must be non-empty string (1-200 characters)
3. `priority` must always be set (default: MEDIUM)
4. `tags` must contain unique tag names (no duplicates per task)
5. `created_at` is set on creation and never modified
6. `updated_at` is set on creation and updated on any modification
7. `tags` values are normalized: lowercase, trimmed whitespace

## 4. CLI Interface

### 4.1 New Commands

#### 4.1.1 `search` Command

**Synopsis:**
```
todo search <keyword> [--status <status>] [--priority <priority>] [--tag <tag>]
```

**Description:**
Search for tasks containing the specified keyword in title or description.

**Arguments:**
- `keyword` (required): Text to search for (case-insensitive)

**Options:**
- `--status ACTIVE|COMPLETED`: Filter by task status
- `--priority HIGH|MEDIUM|LOW`: Filter by priority level
- `--tag TAG`: Filter by specific tag

**Examples:**
```bash
todo search "api"                    # Search all tasks for "api"
todo search "bug" --status ACTIVE    # Search active tasks only
todo search "urgent" --priority HIGH # Search high priority tasks
todo search "project" --tag work     # Search tasks tagged "work"
```

**Output Format:**
```
Found 2 task(s) matching "api":

[1] HIGH [bug] API endpoint returns 500
     id: 1 | status: ACTIVE | priority: HIGH | tags: [bug, backend]
     created: 2026-01-02 10:30 | updated: 2026-01-02 14:15

[2] MEDIUM API documentation
     id: 2 | status: ACTIVE | priority: MEDIUM | tags: [docs]
     created: 2026-01-01 09:00 | updated: 2026-01-01 09:00
```

#### 4.1.2 `filter` Command

**Synopsis:**
```
todo filter [--status <status>] [--priority <priority>] [--tag <tag>]
```

**Description:**
Filter tasks based on specified criteria. Multiple filters are ANDed together.

**Options:**
- `--status ACTIVE|COMPLETED`: Show only tasks with specific status
- `--priority HIGH|MEDIUM|LOW`: Show only tasks with specific priority
- `--tag TAG`: Show only tasks with specific tag

**Examples:**
```bash
todo filter                    # Show all tasks (same as list)
todo filter --status ACTIVE    # Show only active tasks
todo filter --priority HIGH    # Show only high priority tasks
todo filter --tag work         # Show only tasks tagged "work"
todo filter --status ACTIVE --priority HIGH  # AND logic
```

**Output Format:**
```
Filtered 3 task(s) by: status=ACTIVE, priority=HIGH

[1] HIGH Write API spec
     id: 1 | status: ACTIVE | priority: HIGH | tags: [planning]
     created: 2026-01-02 08:00 | updated: 2026-01-02 08:00

[2] HIGH Review PR #42
     id: 2 | status: ACTIVE | priority: HIGH | tags: [review, backend]
     created: 2026-01-02 09:30 | updated: 2026-01-02 11:00

[3] HIGH Database migration
     id: 3 | status: ACTIVE | priority: HIGH | tags: [db, urgent]
     created: 2026-01-01 16:00 | updated: 2026-01-02 07:00
```

#### 4.1.3 `sort` Command

**Synopsis:**
```
todo sort <field> [--reverse]
```

**Description:**
Display tasks sorted by the specified field.

**Arguments:**
- `field` (required): Field to sort by - `title`, `priority`, `id`, `created`

**Options:**
- `--reverse`: Sort in descending order instead of ascending

**Examples:**
```bash
todo sort title           # Sort alphabetically by title (ascending)
todo sort priority        # Sort by priority (HIGH > MEDIUM > LOW)
todo sort id              # Sort by creation order (oldest first)
todo sort created         # Sort by creation date (oldest first)
todo sort title --reverse # Sort alphabetically (descending)
todo sort priority --reverse  # Sort by priority (LOW > MEDIUM > HIGH)
```

**Output Format:**
```
Sorted 3 task(s) by: priority (descending)

[1] HIGH [urgent] Database migration
     id: 3 | status: ACTIVE | priority: HIGH | tags: [db, urgent]
     created: 2026-01-01 16:00 | updated: 2026-01-02 07:00

[2] HIGH Review PR #42
     id: 2 | status: ACTIVE | priority: HIGH | tags: [review, backend]
     created: 2026-01-02 09:30 | updated: 2026-01-02 11:00

[3] MEDIUM Update documentation
     id: 5 | status: ACTIVE | priority: MEDIUM | tags: [docs]
     created: 2026-01-02 10:00 | updated: 2026-01-02 10:00
```

### 4.2 Modified Commands

#### 4.2.1 `add` Command - Extended

**New Synopsis:**
```
todo add <title> [--description <desc>] [--priority <priority>] [--tag <tag>...]
```

**New Options:**
- `--description DESC`: Detailed task description (optional)
- `--priority HIGH|MEDIUM|LOW`: Priority level (default: MEDIUM)
- `--tag TAG`: Tag to add (can be specified multiple times)

**Examples:**
```bash
todo add "Write API spec" --priority HIGH --tag planning --tag backend
todo add "Fix login bug" --priority HIGH --tag bug --description "OAuth flow fails"
todo add "Update docs" --priority LOW --tag docs
```

**Output:**
```
Task added: [5] Write API spec
     priority: HIGH | tags: [planning, backend]
```

#### 4.2.2 `list` Command - Extended

**New Synopsis:**
```
todo list [--extended]
```

**New Options:**
- `--extended`: Show full details including description, priority, and tags

**Examples:**
```bash
todo list                    # Compact format (updated)
todo list --extended         # Full details with priority and tags
```

**Output - Compact (default):**
```
ID  Status    Priority  Title
1   ACTIVE    HIGH      [bug] API endpoint returns 500
2   ACTIVE    MEDIUM    API documentation
3   COMPLETED LOW       Initial setup
```

**Output - Extended:**
```
ID  Status    Priority  Title                      Tags
1   ACTIVE    HIGH      [bug] API endpoint returns 500  [bug, backend]
2   ACTIVE    MEDIUM    API documentation                 [docs]
3   COMPLETED LOW       Initial setup                      []

Showing 3 task(s)
```

#### 4.2.3 `update` Command - Extended

**New Synopsis:**
```
todo update <id> [--title <title>] [--description <desc>] [--priority <priority>] [--add-tag <tag>] [--remove-tag <tag>]
```

**New Options:**
- `--description DESC`: Update task description
- `--priority HIGH|MEDIUM|LOW`: Update priority level
- `--add-tag TAG`: Add a tag (can be specified multiple times)
- `--remove-tag TAG`: Remove a tag (can be specified multiple times)

**Examples:**
```bash
todo update 1 --priority HIGH
todo update 1 --add-tag urgent --remove-tag bug
todo update 1 --description "Detailed description here"
```

**Output:**
```
Task updated: [1] API endpoint returns 500
     priority: HIGH (was MEDIUM) | tags: [urgent, backend] (removed: [bug])
```

### 4.3 Preserved Commands

The following commands remain unchanged:
- `complete <id>` - Mark task as completed
- `incomplete <id>` - Reopen a completed task
- `delete <id>` - Remove a task
- `help` - Show help message

## 5. Acceptance Criteria

### 5.1 Priority Management

- [AC-P001] Tasks can be created with priority HIGH, MEDIUM, or LOW
- [AC-P002] Default priority is MEDIUM when not specified
- [AC-P003] Priority can be updated via `update` command
- [AC-P004] Tasks display priority in all list/search/filter outputs
- [AC-P005] Priority sorting orders: HIGH > MEDIUM > LOW

### 5.2 Tag Management

- [AC-T001] Tasks can have zero or more tags
- [AC-T002] Tags are case-insensitive and stored lowercase
- [AC-T003] Duplicate tags on a single task are not allowed
- [AC-T004] Tags can be added via `add --tag` or `update --add-tag`
- [AC-T005] Tags can be removed via `update --remove-tag`
- [AC-T006] Tasks display tags in all list/search/filter outputs

### 5.3 Search Functionality

- [AC-S001] `search <keyword>` finds tasks where keyword appears in title OR description
- [AC-S002] Search is case-insensitive
- [AC-S003] Search can be combined with `--status`, `--priority`, `--tag` filters
- [AC-S004] Search shows matching keyword context (if possible)
- [AC-S005] Search reports "No matching tasks" when no results

### 5.4 Filter Functionality

- [AC-F001] `filter --status ACTIVE|COMPLETED` shows only matching status
- [AC-F002] `filter --priority HIGH|MEDIUM|LOW` shows only matching priority
- [AC-F003] `filter --tag <tag>` shows only tasks with that tag
- [AC-F004] Multiple filters are ANDed together
- [AC-F005] Filter reports "No matching tasks" when no results

### 5.5 Sort Functionality

- [AC-SO001] `sort title` sorts alphabetically (A-Z)
- [AC-SO002] `sort priority` orders HIGH > MEDIUM > LOW
- [AC-SO003] `sort id` orders by creation order (oldest first)
- [AC-SO004] `sort created` orders by creation date (oldest first)
- [AC-SO005] `--reverse` flag reverses the sort order
- [AC-SO006] Sort displays task count and sort criteria

### 5.6 List Command Enhancement

- [AC-L001] `list` shows compact table with ID, Status, Priority, Title, Tags
- [AC-L002] `list --extended` shows full details including description
- [AC-L003] Tags displayed as comma-separated list in brackets: `[tag1, tag2]`
- [AC-L004] Priority displayed as label: `HIGH`, `MEDIUM`, `LOW`

### 5.7 Add/Update Command Enhancement

- [AC-A001] `add` accepts `--description`, `--priority`, and `--tag` options
- [AC-A002] `update` accepts `--description`, `--priority`, `--add-tag`, `--remove-tag`
- [AC-A003] Output shows what changed (old value -> new value)
- [AC-A004] Tag normalization: lowercase, trimmed whitespace

### 5.8 Data Persistence

- [AC-D001] Priority and tags are persisted to storage
- [AC-D002] No data loss on application restart
- [AC-D003] Task IDs continue to increment correctly

## 6. Error Handling

### 6.1 Validation Errors

| Error Code | Condition | Message |
|------------|-----------|---------|
| ERR-001 | Invalid priority value | "Invalid priority. Must be HIGH, MEDIUM, or LOW." |
| ERR-002 | Invalid status value | "Invalid status. Must be ACTIVE or COMPLETED." |
| ERR-003 | Empty title on add/update | "Task title cannot be empty." |
| ERR-004 | Title too long (>200 chars) | "Task title must be 200 characters or less." |
| ERR-005 | Duplicate tag on add | "Tag '{tag}' already exists on this task." |
| ERR-006 | Tag to remove not found | "Tag '{tag}' not found on this task." |

### 6.2 Operational Errors

| Error Code | Condition | Message |
|------------|-----------|---------|
| ERR-101 | Task ID not found | "Task with ID {id} not found." |
| ERR-102 | No tasks match filter | "No tasks match the specified filter." |
| ERR-103 | No tasks match search | "No tasks found matching '{keyword}'." |
| ERR-104 | Invalid sort field | "Invalid sort field. Must be: title, priority, id, created." |

## 7. Technical Requirements

### 7.1 Repository Changes

```python
class TaskRepository(ABC):
    @abstractmethod
    def find_by_priority(self, priority: Priority) -> list[Task]: ...

    @abstractmethod
    def find_by_tag(self, tag: str) -> list[Task]: ...

    @abstractmethod
    def search(self, keyword: str) -> list[Task]: ...

    @abstractmethod
    def find_by_status(self, status: TaskStatus) -> list[Task]: ...
```

### 7.2 Storage Schema Update

```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Write API spec",
      "description": "Create OpenAPI specification",
      "status": "ACTIVE",
      "priority": "HIGH",
      "tags": ["planning", "backend"],
      "created_at": "2026-01-02T08:00:00",
      "updated_at": "2026-01-02T08:00:00"
    }
  ],
  "next_id": 2
}
```

### 7.3 Service Layer Changes

```python
class TaskService:
    def add_task(self, title: str, description: str = "",
                 priority: Priority = Priority.MEDIUM,
                 tags: list[str] = None) -> Task: ...

    def update_task(self, task_id: int, **kwargs) -> Task: ...

    def search_tasks(self, keyword: str,
                     status: TaskStatus = None,
                     priority: Priority = None,
                     tag: str = None) -> list[Task]: ...

    def filter_tasks(self, status: TaskStatus = None,
                     priority: Priority = None,
                     tag: str = None) -> list[Task]: ...

    def sort_tasks(self, tasks: list[Task], field: str,
                   reverse: bool = False) -> list[Task]: ...
```

## 8. Out of Scope

1. **Tag colors/themes** - Visual customization of tags
2. **Tag aliases** - Alternative names for the same tag
3. **Bulk tag operations** - Add/remove tags on multiple tasks
4. **Task dependencies** - One task depends on another
5. **Due dates** - Tasks with deadlines
6. **Subtasks** - Hierarchical task structures
7. **Task comments/notes** - Extended discussion on tasks
8. **Task templates** - Reusable task patterns
9. **Archive** - Archiving completed tasks
10. **Export** - Export tasks to other formats

## 9. Future Considerations

- Due dates and reminders
- Task dependencies and blocking
- Subtasks and checklists
- Rich task descriptions (markdown)
- Task templates and presets
- Export to CSV/JSON
- Import from external sources
- Task sharing/collaboration
