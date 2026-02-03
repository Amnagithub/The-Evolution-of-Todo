# Feature Specification: CLI State Scope

**Feature Branch**: `001-cli-state-scope`
**Created**: 2025-01-01
**Status**: Draft
**Input**: User description: "update CLI spec: State Scope: Tasks are stored in memory and exist only during the execution of a single CLI invocation. Each command runs in isolation."

**Update**: 2025-01-01 - Relaxed constraint: Tasks now persist within a terminal session using file-based storage.

## User Scenarios & Testing

### User Story 1 - Session-Based Task Persistence (Priority: P1)

A user executes multiple commands in sequence within a single terminal session. Tasks created in earlier commands remain available in later commands.

**Acceptance Scenarios**:
1. **Given** the user runs `todo add "Buy groceries"`, **When** they run `todo list`, **Then** the task appears in the list
2. **Given** a task was created, **When** the user runs `todo complete 1`, **Then** the task status changes to complete
3. **Given** multiple tasks exist, **When** the user runs `todo list`, **Then** all tasks appear with correct status indicators

---

### User Story 2 - New Terminal Session Starts Fresh (Priority: P2)

A user closes their terminal and opens a new one. Tasks from the previous session are not visible.

**Acceptance Scenarios**:
1. **Given** tasks were created in terminal session A, **When** the user opens terminal session B and runs `todo list`, **Then** no tasks are displayed (new session starts fresh)

---

## Requirements

### Functional Requirements

- **FR-001**: System MUST persist tasks across CLI invocations within the same terminal session
- **FR-002**: Each command execution MUST read/write to the shared task store
- **FR-003**: Tasks created during a session MUST remain available for subsequent commands
- **FR-004**: New terminal sessions start with an empty task list (no cross-session persistence)
- **FR-005**: System MUST operate correctly with persistent task data on each invocation

### Key Entities

- **Session Storage**: A file-based storage (`.todo/tasks.json`) that persists task data across commands within a terminal session

---

## State Scope Constraint

### Session-Based Storage

Tasks are stored in a file-based storage (`.todo/tasks.json`) that persists across CLI invocations within a terminal session:

1. **Tasks persist within a session**: When a user runs `todo add`, then `todo list`, the task appears in the list
2. **Cross-command state sharing**: Multiple commands in sequence share the same task store
3. **Session isolation**: Each terminal session has its own storage file in its working directory
4. **Process-based lifecycle**: Tasks exist as long as the terminal session is active

### Example Behavior

```bash
$ todo add "Buy groceries"
Task #1 added: Buy groceries

$ todo list
ID  | Title         | Status    | Created
----|---------------|-----------|----------
1   | Buy groceries | Incomplete| ...

$ todo complete 1
Task #1 marked complete

$ todo list
ID  | Title         | Status    | Created
----|---------------|-----------|----------
1   | Buy groceries | Complete  | ...
```

---

## Out of Scope

- Cross-session task sharing (tasks don't persist when terminal closes)
- Cloud sync or remote storage
- Multi-user support
