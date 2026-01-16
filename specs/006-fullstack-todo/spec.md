# Feature Specification: Phase II - Full-Stack Todo Web Application

**Feature Branch**: `006-fullstack-todo`
**Created**: 2026-01-15
**Status**: Draft
**Input**: User description: "Transform console todo app into multi-user web app with CRUD persistence, JWT auth for user isolation"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - User Registration and Authentication (Priority: P1)

A new user visits the application and creates an account to start managing their personal tasks. After registration, they can sign in securely and their identity persists across sessions.

**Why this priority**: Authentication is foundational - no other feature works without user identity. Users cannot create or view tasks without being authenticated first.

**Independent Test**: Can be fully tested by completing signup flow, receiving confirmation, then signing in with credentials. Delivers secure user identity management.

**Acceptance Scenarios**:

1. **Given** a visitor on the signup page, **When** they enter valid email and password, **Then** an account is created and they are signed in automatically
2. **Given** a registered user on the signin page, **When** they enter correct credentials, **Then** they are authenticated and redirected to their task dashboard
3. **Given** an authenticated user, **When** they close the browser and return, **Then** their session persists via stored JWT token
4. **Given** a user with invalid credentials, **When** they attempt to sign in, **Then** they receive a clear error message without revealing which field is incorrect

---

### User Story 2 - Create and View Tasks (Priority: P1)

An authenticated user creates new tasks with titles and optional descriptions. They can view all their tasks in a list, seeing only tasks they own.

**Why this priority**: Core value proposition - users need to create and see their tasks. This is the minimum viable product functionality.

**Independent Test**: Can be fully tested by creating 3 tasks and verifying they appear in the list. Another user's tasks should never appear.

**Acceptance Scenarios**:

1. **Given** an authenticated user on the tasks page, **When** they enter a task title and submit, **Then** the task is created and appears in their task list
2. **Given** an authenticated user with existing tasks, **When** they view the tasks page, **Then** they see only their own tasks sorted by creation date (newest first)
3. **Given** an authenticated user, **When** they create a task with title and description, **Then** both fields are saved and displayed
4. **Given** an unauthenticated visitor, **When** they attempt to access the tasks page, **Then** they are redirected to the signin page

---

### User Story 3 - Update Tasks (Priority: P2)

An authenticated user modifies existing tasks by editing the title, description, or marking completion status.

**Why this priority**: Essential for task lifecycle management but depends on tasks existing first (P1).

**Independent Test**: Can be fully tested by creating a task, then editing its title/description and verifying changes persist.

**Acceptance Scenarios**:

1. **Given** an authenticated user viewing their task, **When** they edit the title and save, **Then** the updated title is persisted and displayed
2. **Given** an authenticated user viewing their task, **When** they toggle the completed status, **Then** the completion state changes and persists
3. **Given** an authenticated user, **When** they attempt to update another user's task, **Then** the request is rejected with 404 (task not found for this user)

---

### User Story 4 - Delete Tasks (Priority: P2)

An authenticated user permanently removes tasks they no longer need.

**Why this priority**: Completes CRUD operations but lower priority than create/read/update.

**Independent Test**: Can be fully tested by creating a task, deleting it, and verifying it no longer appears in the list.

**Acceptance Scenarios**:

1. **Given** an authenticated user viewing their task, **When** they click delete and confirm, **Then** the task is permanently removed from their list
2. **Given** an authenticated user, **When** they attempt to delete another user's task, **Then** the request is rejected with 404

---

### User Story 5 - View Individual Task Details (Priority: P3)

An authenticated user views the full details of a specific task by its ID.

**Why this priority**: Nice-to-have for detailed view but list view covers most use cases.

**Independent Test**: Can be fully tested by creating a task with description, then viewing it by ID and verifying all fields display.

**Acceptance Scenarios**:

1. **Given** an authenticated user, **When** they request a specific task by ID, **Then** they see the full task details (title, description, completed status, timestamps)
2. **Given** an authenticated user, **When** they request a task ID that doesn't exist or belongs to another user, **Then** they receive a 404 response

---

### Edge Cases

- What happens when a user creates a task with an empty title? → Validation error, title is required (1-200 characters)
- What happens when a user's JWT token expires? → User is redirected to signin page; API returns 401
- What happens when a user creates a task with only whitespace? → Validation error, title must contain non-whitespace characters
- How does the system handle concurrent task updates? → Last write wins; optimistic concurrency acceptable for MVP
- What happens when the database is unavailable? → User sees friendly error message; API returns 503
- What happens when a user signs out? → JWT token is cleared from local storage; user redirected to signin page

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to register with email and password via Better Auth
- **FR-002**: System MUST authenticate users and issue JWT tokens upon successful signin
- **FR-003**: System MUST validate JWT tokens on every protected API request via Authorization header
- **FR-004**: System MUST reject requests without valid JWT with 401 Unauthorized
- **FR-005**: System MUST allow authenticated users to create tasks with title (required, 1-200 chars) and description (optional)
- **FR-006**: System MUST automatically associate created tasks with the authenticated user's ID
- **FR-007**: System MUST allow authenticated users to list only their own tasks
- **FR-008**: System MUST allow authenticated users to retrieve a single task by ID (only if they own it)
- **FR-009**: System MUST allow authenticated users to update their own tasks (title, description)
- **FR-010**: System MUST allow authenticated users to toggle task completion status via PATCH endpoint
- **FR-011**: System MUST allow authenticated users to delete their own tasks
- **FR-012**: System MUST filter all task queries by authenticated user_id (no path-based user ID allowed)
- **FR-013**: System MUST persist all data to Neon Postgres database
- **FR-014**: System MUST run frontend on port 3000 and backend on port 8000 via docker-compose

### Key Entities

- **User**: Represents an authenticated user; managed by Better Auth; has unique ID, email, password hash
- **Task**: Represents a todo item owned by a user; attributes include ID, title (required), description (optional), completed status (boolean, default false), user_id (foreign key), created_at, updated_at timestamps

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can complete registration and signin in under 60 seconds
- **SC-002**: Users can create a new task in under 10 seconds (from page load to task visible in list)
- **SC-003**: All 6 API endpoints (GET list, POST, GET by ID, PUT, DELETE, PATCH complete) respond correctly based on authentication
- **SC-004**: System correctly isolates user data - User A cannot see, modify, or delete User B's tasks (100% isolation)
- **SC-005**: Application starts successfully with single `docker-compose up` command
- **SC-006**: Frontend is responsive and usable on desktop browsers (Chrome, Firefox, Safari)
- **SC-007**: System handles at least 100 concurrent authenticated users without errors
- **SC-008**: Invalid authentication attempts return appropriate error within 2 seconds

## Assumptions

- Better Auth is the chosen authentication library for the frontend (Next.js)
- JWT tokens are shared between frontend (Better Auth) and backend (FastAPI) using a shared secret (BETTER_AUTH_SECRET)
- Backend validates JWT tokens using PyJWT library
- Neon Postgres is accessed via connection pooling (neon proxy)
- SQLModel is used for ORM in the FastAPI backend
- No email verification required for MVP (can be added later)
- Password requirements follow Better Auth defaults
- Session duration follows Better Auth JWT defaults (tokens expire, refresh handled by Better Auth)

## Constraints

- Monorepo structure: /specs/*, /frontend, /backend, docker-compose.yml
- Tech stack fixed: Next.js 14+ (App Router), FastAPI/SQLModel, Neon Postgres, Better Auth (JWT)
- Security: JWT shared secret via environment variable; no path-based user_id; header-only authentication
- No manual coding: Implementation via Claude Code with spec references (@specs/features/task-crud.md)

## Out of Scope

- Phase I console application (already exists)
- Phase III chatbot features
- Email verification for registration
- Password reset functionality
- Social authentication (OAuth providers)
- Task categories, tags, or priorities
- Task due dates or reminders
- Task sharing between users
- Mobile-specific responsive design
- Offline functionality
