# Feature Specification: AI Todo Chatbot (Phase III)

**Feature Branch**: `001-ai-todo-chatbot`
**Created**: 2026-02-05
**Status**: Draft
**Input**: Phase III AI Todo Chatbot - Natural language todo management with MCP tools, stateless architecture, conversation persistence, and animated ChatKit UI integrated with Phase II app.

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Add Task via Natural Language (Priority: P1)

As a user, I want to add a task by typing natural phrases like "add buy groceries" or "remember to call mom" so that I can quickly capture todos without navigating forms.

**Why this priority**: Core functionality - task creation is the foundational operation for any todo app. Without this, no other features have value.

**Independent Test**: Can be tested by sending a chat message like "add buy milk" and verifying a task is created with title "buy milk" in the database.

**Acceptance Scenarios**:

1. **Given** an authenticated user in the chat interface, **When** they type "add buy groceries", **Then** a task with title "buy groceries" is created and the assistant confirms with "Added buy groceries (ID 1) ✓" with fade-in animation and green check icon.
2. **Given** an authenticated user, **When** they type "remember to call doctor tomorrow", **Then** a task with title "call doctor tomorrow" is created and confirmed.
3. **Given** an authenticated user, **When** they type "add" with no title, **Then** the assistant responds with a friendly validation error: "Please give me a valid title (max 255 chars for title)."
4. **Given** an authenticated user, **When** they type "I need to finish the report", **Then** a task with title "finish the report" is created.

---

### User Story 2 - List Tasks with Filters (Priority: P1)

As a user, I want to view my tasks by saying "show my tasks" or "what's pending?" so that I can see what I need to work on.

**Why this priority**: Core functionality - users must be able to see their tasks to manage them effectively.

**Independent Test**: Can be tested by listing tasks and verifying the returned list matches tasks in the database for the authenticated user.

**Acceptance Scenarios**:

1. **Given** a user with 3 tasks (2 pending, 1 completed), **When** they say "show my tasks", **Then** all 3 tasks are displayed with staggered fade-up animation (0.1s delay between items).
2. **Given** a user with tasks, **When** they say "what's pending?", **Then** only pending tasks are listed.
3. **Given** a user with tasks, **When** they say "show completed tasks", **Then** only completed tasks are listed.
4. **Given** a user with no tasks, **When** they say "list my tasks", **Then** the assistant responds "Here are your tasks:" followed by an empty list indicator.

---

### User Story 3 - Complete Task by Name or ID (Priority: P1)

As a user, I want to mark a task as done by saying "done buy groceries" or "complete task 5" so that I can track my progress.

**Why this priority**: Core functionality - completing tasks is essential for task management workflow.

**Independent Test**: Can be tested by completing a task and verifying its status changes to "completed" in the database.

**Acceptance Scenarios**:

1. **Given** a user with a pending task "buy groceries" (ID 5), **When** they say "done buy groceries", **Then** the agent chains: list_tasks → finds match → complete_task, and confirms "Marked buy groceries as done ✓" with strike-through and green checkmark animation.
2. **Given** a user with task ID 5, **When** they say "complete task 5", **Then** the task is marked complete directly.
3. **Given** a user with multiple tasks containing "report", **When** they say "done report", **Then** the agent asks for clarification: "I found multiple tasks matching 'report'. Which one did you mean?"
4. **Given** a user references a non-existent task, **When** they say "done nonexistent task", **Then** the assistant responds: "I couldn't find a task matching 'nonexistent task'. Want me to list your current tasks?"
5. **Given** a task already completed, **When** the user tries to complete it again, **Then** the assistant indicates it's already completed.

---

### User Story 4 - Delete Task (Priority: P2)

As a user, I want to delete a task by saying "delete buy groceries" or "remove task 3" so that I can clean up my task list.

**Why this priority**: Important for task management but secondary to core CRUD operations.

**Independent Test**: Can be tested by deleting a task and verifying it no longer exists in the database.

**Acceptance Scenarios**:

1. **Given** a user with task "old item" (ID 3), **When** they say "delete old item", **Then** the task is removed and confirmed with "Removed old item" with fade-out and red trash icon pulse animation.
2. **Given** a user with task ID 3, **When** they say "remove task 3", **Then** the task is deleted directly.
3. **Given** a non-existent task reference, **When** the user says "delete phantom task", **Then** the assistant offers recovery: "I couldn't find a task matching 'phantom task'. Want me to list your current tasks?"

---

### User Story 5 - Update Task (Priority: P2)

As a user, I want to update a task's title or description by saying "rename task 5 to new title" so that I can correct or refine my tasks.

**Why this priority**: Useful for refinement but users can work around this by deleting and re-adding.

**Independent Test**: Can be tested by updating a task and verifying the new title/description in the database.

**Acceptance Scenarios**:

1. **Given** a user with task "buy milk" (ID 2), **When** they say "change buy milk to buy almond milk", **Then** the task title is updated and confirmed with "Updated to buy almond milk" with text highlight and scale-up animation.
2. **Given** no changes provided, **When** the user says "update task 2", **Then** the assistant responds: "Looks like nothing changed - did you want to update something?"
3. **Given** a task by name, **When** the user says "rename groceries to grocery shopping", **Then** the agent chains list → match → update.

---

### User Story 6 - View Profile Information (Priority: P3)

As a user, I want to ask "who am I?" or "my profile" to see basic account information so that I can verify my identity.

**Why this priority**: Nice-to-have feature for user context, not critical for task management.

**Independent Test**: Can be tested by requesting profile and verifying username and creation date are returned (no sensitive data).

**Acceptance Scenarios**:

1. **Given** an authenticated user "john_doe" created on 2025-01-15, **When** they say "who am I?", **Then** the assistant responds "You are john_doe (created 2025-01-15)" with profile card slide-in animation.
2. **Given** any user, **When** they ask for profile, **Then** no sensitive data (passwords, tokens, recovery codes) is ever returned.

---

### User Story 7 - Animated Chat Experience (Priority: P1)

As a user, I want a smooth, animated chat interface so that the interaction feels responsive and engaging.

**Why this priority**: Critical for user experience - animations provide feedback and polish.

**Independent Test**: Can be tested by performing actions and verifying animations occur within timing requirements.

**Acceptance Scenarios**:

1. **Given** a user sends a message, **When** the message is submitted, **Then** it slides in from the right with 300ms ease-out animation.
2. **Given** the assistant is processing, **When** thinking begins, **Then** animated typing dots (3 bouncing dots) appear.
3. **Given** a tool is being called, **When** processing occurs, **Then** a small spinner appears next to "Thinking..."
4. **Given** a successful action, **When** confirmed, **Then** a green checkmark appears with optional subtle confetti.
5. **Given** an error occurs, **When** displayed, **Then** message has red border with gentle horizontal shake (150ms).
6. **Given** user has prefers-reduced-motion enabled, **When** any animation would occur, **Then** fall back to simple fade only.
7. **Given** mobile device, **When** keyboard opens, **Then** chat stays visible above keyboard without overlapping Phase II nav.

---

### User Story 8 - Conversation Persistence (Priority: P1)

As a user, I want my conversation history to persist across sessions so that I can see previous interactions after restarting the app.

**Why this priority**: Critical for stateless server architecture - all state must survive restarts.

**Independent Test**: Can be tested by having a conversation, restarting the server, and verifying history is preserved.

**Acceptance Scenarios**:

1. **Given** a user has a conversation, **When** the server restarts, **Then** all previous messages are preserved and visible on reload.
2. **Given** conversation history in the database, **When** user opens chat, **Then** history is loaded and displayed.

---

### Edge Cases

- What happens when a user tries to manage another user's tasks? → Returns unauthorized error: "I can only work with your own tasks, sorry."
- What happens when the database is temporarily unavailable? → Graceful error with retry suggestion.
- What happens when task title exceeds 255 characters? → Validation error with friendly message.
- What happens when session expires mid-conversation? → Prompt to re-authenticate.
- What happens with network latency causing delayed animations? → Animations complete naturally; skeleton states for long waits.
- What happens when multiple fuzzy matches exist for a task name? → Agent asks user to clarify which task they meant.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to create tasks via natural language commands (add, create, remember, I need to)
- **FR-002**: System MUST list tasks with optional filtering by status (all, pending, completed)
- **FR-003**: System MUST mark tasks as completed by ID or fuzzy name match
- **FR-004**: System MUST delete tasks by ID or fuzzy name match
- **FR-005**: System MUST update task title and/or description by ID or fuzzy name match
- **FR-006**: System MUST return non-sensitive user profile information (username, created_at)
- **FR-007**: System MUST persist all conversation history in the database
- **FR-008**: System MUST enforce user ownership on all tool operations (user_id validation)
- **FR-009**: System MUST chain tool calls when user references tasks by name (list → match → target operation)
- **FR-010**: System MUST ask for clarification when multiple fuzzy matches exist
- **FR-011**: System MUST never return sensitive user data (passwords, tokens, recovery codes)
- **FR-012**: System MUST provide friendly error messages with recovery paths
- **FR-013**: System MUST reuse Better Auth from Phase II for authentication
- **FR-014**: System MUST be completely stateless (all state in PostgreSQL)
- **FR-015**: System MUST provide animated UI feedback for all user interactions
- **FR-016**: System MUST respect prefers-reduced-motion accessibility setting
- **FR-017**: System MUST ensure chat remains usable on mobile (above keyboard, no nav overlap)

### Key Entities

- **Task**: Represents a user's todo item. Attributes: id, user_id (FK to User), title (max 255 chars), description (optional), completed (boolean), created_at, updated_at.
- **User**: Represents an authenticated user (reused from Phase II). Attributes: id, username, email, created_at. No sensitive fields exposed.
- **Conversation Message**: Represents a single message in chat history. Attributes: id, user_id, role (user/assistant), content, tool_calls (optional), created_at.
- **MCP Tool**: Represents an available operation. Tools: add_task, list_tasks, complete_task, delete_task, update_task, get_user_details.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can add a task via chat in under 3 seconds from message send to confirmation display
- **SC-002**: All UI animations complete within 400ms maximum
- **SC-003**: System supports at least 100 concurrent chat users without degradation
- **SC-004**: 95% of natural language commands are correctly interpreted on first attempt
- **SC-005**: Conversation history loads within 1 second on session resume
- **SC-006**: 100% of tool operations enforce user ownership (no cross-user data access)
- **SC-007**: Zero sensitive data exposure in any user-facing response
- **SC-008**: Mobile chat remains functional with soft keyboard open
- **SC-009**: System maintains state after server restart (stateless architecture verified)
- **SC-010**: Users with prefers-reduced-motion see fallback animations only

---

## Non-Functional Requirements

| Aspect | Requirement |
|--------|-------------|
| Server state | Completely stateless - all state in Neon PostgreSQL |
| Authentication | Reuse Better Auth from Phase II; every tool enforces user ownership |
| Conversation persistence | Survives server restart/redeploy |
| Tool chaining | Agent chains list → target tool when user references task by name |
| Error handling | Graceful, user-friendly, offers recovery paths |
| UI animations | Message fade-in, typing indicator, tool-call spinner, success check, error shake |
| Performance | Animations ≤ 400ms, support prefers-reduced-motion, no jank on mobile |
| Security | No sensitive user data returned (passwords, tokens, recovery codes) |

---

## MCP Tool Definitions

| Tool | Purpose | Required Params | Optional Params | Success Return | Error Cases | UI Animation |
|------|---------|-----------------|-----------------|----------------|-------------|--------------|
| add_task | Create new task | user_id, title | description | {task_id, status:"created", title} | empty title, unauthorized, title > 255 | Fade-in + green check |
| list_tasks | List tasks (filtered) | user_id | status (all/pending/completed) | Array of task objects or [] | invalid status | Staggered fade-up |
| complete_task | Mark task complete | user_id, task_id | - | {task_id, status:"completed", title} | not found, already completed, unauthorized | Strike-through + green check |
| delete_task | Remove task | user_id, task_id | - | {task_id, status:"deleted", title} | not found, unauthorized | Fade-out + trash pulse |
| update_task | Change title/description | user_id, task_id | title, description | {task_id, status:"updated", title} | no changes, not found, unauthorized | Highlight + scale-up |
| get_user_details | Show non-sensitive profile | user_id | - | {user_id, username, created_at} | user_id mismatch, session expired | Profile card slide-in |

**Security Rule (Non-Negotiable)**: If provided user_id != authenticated_user.id → return `{"error":"unauthorized", "message":"You can only manage your own data"}`

---

## Agent Behavior Specification

| User Intent | Primary Tool | Chaining | Confirmation Template | Animation |
|-------------|--------------|----------|----------------------|-----------|
| "add...", "create...", "remember to...", "I need to..." | add_task | No | "Added {title} (ID {task_id}) ✓" | Fade-in + green check |
| "show/list my tasks", "what's pending?", "all tasks" | list_tasks | No | "Here are your {status} tasks:" | Staggered fade-up |
| "done", "complete", "mark as done", "check off [id/name]" | complete_task | Yes (if name) | "Marked {title} as done ✓" | Strike-through + green check |
| "delete/remove/cancel [id/name]" | delete_task | Yes (if name) | "Removed {title}" | Fade-out + trash pulse |
| "change/update/edit/rename [id/name] to..." | update_task | Yes (if name) | "Updated to {new_title}" | Highlight + scale-up |
| "who am I?", "my profile", "user id", "account info" | get_user_details | No | "You are {username} (created {created_at})" | Profile card slide-in |

**Chaining Rule**: When user references task by name/description instead of ID → agent calls list_tasks → fuzzy match → if unique match → call target tool → if multiple → ask user to clarify.

**Error Response Patterns**:
- Task not found → "I couldn't find a task matching '{name/id}'. Want me to list your current tasks?"
- Unauthorized → "I can only work with your own tasks, sorry."
- Validation fail → "Please give me a valid {field} (max 255 chars for title)."
- No changes in update → "Looks like nothing changed - did you want to update something?"

---

## Frontend Requirements - Animated Chat UI

**Placement**: Bottom-right floating widget (recommended) or dedicated /chat route

**Required Animations**:
- User message: slide in from right, 300ms ease-out
- Assistant thinking: animated typing dots (3 bouncing dots)
- Tool call in progress: small spinner next to "Thinking..."
- Success confirmation: green checkmark + optional subtle confetti
- Error message: red border + gentle horizontal shake (150ms)
- New task added/completed: task item appears with scale-up + fade

**Accessibility**: Respect prefers-reduced-motion → fall back to simple fade only

**Mobile**: Chat stays visible above keyboard, no overlap with Phase II nav

---

## Assumptions

- Phase II Better Auth is fully functional and provides user_id extraction from session
- Phase II database connection and schema are available for extension
- Phase II design system (colors, typography, spacing) will be reused
- Neon PostgreSQL is the database provider
- OpenAI Agents SDK will be used for agent orchestration
- MCP SDK will be used for tool definitions
- ChatKit or similar component library will be used for chat UI base

---

## Out of Scope

- Task due dates, reminders, or scheduling
- Task categories, tags, or projects
- Task sharing or collaboration
- Voice input
- Offline support
- Push notifications
- Task attachments or images
- Recurring tasks
- Task priorities beyond completion status
