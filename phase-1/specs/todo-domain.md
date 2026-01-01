# Feature Specification: Todo Domain Model

**Feature Branch**: `001-todo-domain`
**Created**: 2025-12-30
**Status**: Draft
**Input**: User description: "Define the core business domain model for the Phase 1 Todo application"

## User Scenarios & Testing

### User Story 1 - Task Creation (Priority: P1)

A user can create a new task with a title and optional description. The system assigns a unique ID and marks the task as pending.

**Acceptance Scenarios**:
1. **Given** the system is ready, **When** a user creates a task with title "Buy groceries", **Then** a task with ID 1 is created with status "pending"
2. **Given** a task is being created, **When** the title is empty, **Then** a validation error is raised
3. **Given** a task is being created, **When** the title exceeds 500 characters, **Then** a validation error is raised

---

### User Story 2 - Task Status Management (Priority: P1)

A user can change the status of a task between "pending" and "completed".

**Acceptance Scenarios**:
1. **Given** a pending task exists, **When** the user marks it complete, **Then** status changes to "completed" and completed_at is set
2. **Given** a completed task exists, **When** the user reopens it, **Then** status changes to "pending" and completed_at is cleared
3. **Given** an invalid task ID is provided, **When** status is changed, **Then** a TaskNotFoundError is raised

---

### User Story 3 - Task Retrieval (Priority: P1)

A user can retrieve tasks by ID or list all tasks.

**Acceptance Scenarios**:
1. **Given** tasks exist in the system, **When** a user requests a specific task by ID, **Then** the task is returned
2. **Given** no task exists with the ID, **When** retrieval is attempted, **Then** None is returned
3. **Given** multiple tasks exist, **When** a user requests all tasks, **Then** a list of all tasks is returned in ID order

---

### User Story 4 - Task Deletion (Priority: P2)

A user can permanently remove a task from the system.

**Acceptance Scenarios**:
1. **Given** a task exists, **When** the user deletes it, **Then** the task is permanently removed
2. **Given** a task ID doesn't exist, **When** deletion is attempted, **Then** TaskNotFoundError is raised

---

## Requirements

### Functional Requirements

- **FR-001**: System MUST create tasks with sequential integer IDs starting at 1
- **FR-002**: System MUST validate task title (1-500 characters, non-empty)
- **FR-003**: System MUST support optional task description (0-2000 characters)
- **FR-004**: System MUST track task status (pending/completed)
- **FR-005**: System MUST track creation timestamp for each task
- **FR-006**: System MUST track completion timestamp for completed tasks
- **FR-007**: System MUST generate TaskNotFoundError for invalid IDs
- **FR-008**: System MUST generate ValidationError for invalid inputs
- **FR-009**: System MUST support task deletion by ID
- **FR-010**: System MUST support task updates (title and/or description)
- **FR-011**: System MUST NOT reuse IDs after task deletion

### Key Entities

- **Task**: Core domain entity with id, title, description, status, created_at, completed_at
- **TaskStatus**: Value object with states PENDING and COMPLETED
- **TaskRepository**: In-memory storage interface for CRUD operations
- **TaskService**: Business logic layer coordinating repository operations

### Success Criteria

- **SC-001**: Task creation with valid input succeeds in under 100ms
- **SC-002**: Task operations (create, read, update, delete) are atomic
- **SC-003**: Task IDs are unique and sequential across session
- **SC-004**: 100% of domain logic is unit testable

## Assumptions

- Single-user, single-session context (Phase I)
- Tasks fit in memory (no persistence requirement in Phase I)
- IDs are never reused (prevents confusion in client code)
- Timestamps use UTC timezone
- Maximum concurrent tasks: 10,000 (per spec)

## Out of Scope

- Multi-user support
- Task sharing/collaboration
- Task categories or tags
- Due dates or reminders
- Recurring tasks
- Undo/redo functionality
