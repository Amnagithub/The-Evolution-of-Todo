# Feature Specification: Interactive Session Mode

**Feature Branch**: `005-interactive-session-mode`
**Created**: 2026-01-02
**Status**: Draft
**Input**: User description: "Extend the Phase I Todo CLI to support an interactive session mode that preserves in-memory task state for the lifetime of a single process, without introducing persistence."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Interactive Session Entry (Priority: P1)

As a user who frequently adds and manages multiple tasks,
I want to enter an interactive session where I can run multiple commands while data persists,
So that I can avoid re-running commands and manage tasks efficiently in a continuous workflow.

**Why this priority**: This is the core feature enabling all other interactive behaviors. Without session entry, users cannot benefit from in-memory state persistence.

**Independent Test**: Can be fully tested by running `uv run todo` without arguments and verifying the prompt `> ` appears.

**Acceptance Scenarios**:

1. **Given** the todo application is installed, **When** user runs `uv run todo` without any arguments, **Then** the application enters interactive session mode with a `> ` prompt displayed.
2. **Given** the todo application is installed, **When** user runs `uv run todo add "task"` with arguments, **Then** the command executes in stateless mode and exits (existing behavior preserved).

---

### User Story 2 - Session State Persistence (Priority: P1)

As an interactive user,
I want task data to persist across multiple commands within the same session,
So that I can add, list, complete, and update tasks without losing data between commands.

**Why this priority**: This is the primary value proposition - eliminating the stateless limitation of non-interactive mode.

**Independent Test**: Can be fully tested by adding a task, listing tasks, and verifying the task appears in subsequent list commands within the same session.

**Acceptance Scenarios**:

1. **Given** the user is in an interactive session, **When** user adds a task with `add "shopping" groceries`, **Then** the task is stored in memory with ID 1.
2. **Given** the user has added a task in the session, **When** user runs `list`, **Then** the previously added task is displayed.
3. **Given** the user has completed a task in the session, **When** user lists tasks again, **Then** the task status is updated.
4. **Given** the user has multiple tasks in the session, **When** user adds another task, **Then** both tasks persist in memory.

---

### User Story 3 - Session Exit (Priority: P1)

As an interactive user,
I want to exit the session cleanly with a simple command,
So that I know when my session has ended and my temporary data is discarded.

**Why this priority**: Users need a clear, predictable way to end the session.

**Independent Test**: Can be fully tested by typing `exit` or `quit` and verifying the session ends.

**Acceptance Scenarios**:

1. **Given** the user is in an interactive session, **When** user types `exit`, **Then** the session terminates and returns to the shell.
2. **Given** the user is in an interactive session, **When** user types `quit`, **Then** the session terminates and returns to the shell.
3. **Given** the user has created tasks and exited the session, **When** user starts a new session with `uv run todo`, **Then** no tasks from the previous session are present (state discarded).

---

### User Story 4 - Command Syntax Consistency (Priority: P2)

As an interactive user familiar with the CLI,
I want to use the same command syntax in interactive mode as in non-interactive mode,
So that I don't need to learn new syntax or remember special rules.

**Why this priority**: Consistency reduces cognitive load and allows users to transfer knowledge between modes.

**Independent Test**: Can be fully tested by verifying each command produces identical output in both modes.

**Acceptance Scenarios**:

1. **Given** the user is in an interactive session, **When** user runs `add "task" --priority HIGH`, **Then** the output matches non-interactive mode: `Task added: [1] task\npriority: HIGH | tags: []`.
2. **Given** the user is in an interactive session, **When** user runs `list --extended`, **Then** output format matches non-interactive mode.
3. **Given** the user is in an interactive session, **When** user runs commands, **Then** all output is displayed to stdout.

---

### Edge Cases

- What happens when the user types an empty line (just presses Enter)?
- How does the system handle unrecognized commands in interactive mode?
- What happens with very long input lines or special characters?
- How does Ctrl+C (SIGINT) behave in interactive mode?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: When the todo command is executed without arguments, the application MUST enter interactive session mode.
- **FR-002**: In interactive mode, the application MUST maintain task data in memory for the lifetime of the session.
- **FR-003**: The application MUST accept one command per line from stdin.
- **FR-004**: The application MUST display a prompt using `> ` to indicate readiness for input.
- **FR-005**: The application MUST exit interactive mode when the user types `exit` or `quit`.
- **FR-006**: Upon session exit, all task data MUST be discarded (no persistence).
- **FR-007**: All existing commands (add, list, complete, incomplete, update, delete, help) MUST function identically in interactive and non-interactive modes.
- **FR-008**: Non-interactive commands (with arguments) MUST remain stateless (existing behavior preserved).
- **FR-009**: The application MUST NOT write any data to the file system or database during interactive sessions.

### Key Entities

- **Interactive Session**: Represents a single execution instance of the todo CLI in interactive mode, containing a reference to a TaskService with in-memory repository.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can execute multiple commands within a single `uv run todo` session and task data persists across all commands.
- **SC-002**: Task data is not accessible after session exit (zero leakage between sessions).
- **SC-003**: Existing non-interactive command behavior remains unchanged (100% backward compatibility).
- **SC-004**: All commands that work non-interactively work identically in interactive mode (100% feature parity).

### Non-Functional Requirements

- **NFR-001**: Session mode MUST NOT introduce any file system or network dependencies.
- **NFR-002**: Memory usage MUST be bounded by the number of tasks created during the session.

## Assumptions

- The existing CLI structure with ArgumentParser can be reused by parsing individual lines.
- The existing TaskService and InMemoryTaskRepository can be instantiated once per session.
- Line editing capabilities (backspace, arrow keys) are nice-to-have but not required for MVP.

## Out of Scope

- Persistence across executions (this is explicitly forbidden).
- Background daemon mode.
- Configuration options or flags for interactive mode.
- History navigation or command recall.
- Multi-user or concurrent access.
- Remote or distributed session support.
