# Tasks: AI Todo Chatbot (Phase III)

**Input**: Design documents from `/specs/001-ai-todo-chatbot/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Tests included as spec mentions pytest suite requirement.

**Organization**: Tasks grouped by user story for independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1-US8)
- All paths relative to repository root

## User Story Mapping

| Story | Title | Priority | Tools Required |
|-------|-------|----------|----------------|
| US1 | Add Task via Natural Language | P1 | add_task |
| US2 | List Tasks with Filters | P1 | list_tasks |
| US3 | Complete Task by Name or ID | P1 | complete_task + chaining |
| US4 | Delete Task | P2 | delete_task + chaining |
| US5 | Update Task | P2 | update_task + chaining |
| US6 | View Profile Information | P3 | get_user_details |
| US7 | Animated Chat Experience | P1 | (frontend only) |
| US8 | Conversation Persistence | P1 | (database + API) |

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization, dependencies, and basic structure

- [X] T001 Add openai and mcp dependencies to backend/requirements.txt
- [X] T002 [P] Add framer-motion dependency to frontend/package.json
- [X] T003 [P] Update backend/.env.example with OPENAI_API_KEY and OPENAI_MODEL
- [X] T004 [P] Create backend/tools/ directory with __init__.py
- [X] T005 [P] Create backend/agent/ directory with __init__.py
- [X] T006 [P] Create frontend/components/chat/ directory with index.ts

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Database models, base tool infrastructure, chat API structure, and basic UI shell

**⚠️ CRITICAL**: All user stories depend on this phase completing first

### Database Models (US8 Dependency)

- [X] T007 [P] Create Conversation SQLModel in backend/models/conversation.py
- [X] T008 [P] Create Message SQLModel in backend/models/message.py
- [X] T009 Create Alembic migration for conversation and message tables in backend/migrations/
- [X] T010 Run migration and verify tables created in Neon PostgreSQL

### MCP Tool Base Infrastructure

- [X] T011 Create tool base class and context in backend/tools/base.py
- [X] T012 [P] Create tool response schemas (success/error) in backend/tools/schemas.py

### Chat API Structure

- [X] T013 Create chat router skeleton in backend/routes/chat.py
- [X] T014 Register chat router in backend/main.py
- [X] T015 [P] Create chat API client in frontend/lib/chat-api.ts
- [X] T016 [P] Create useChat hook skeleton in frontend/hooks/useChat.ts

### Chat UI Shell (US7 Foundation)

- [X] T017 [P] Create ChatWidget container component in frontend/components/chat/ChatWidget.tsx
- [X] T018 [P] Create ChatInput component in frontend/components/chat/ChatInput.tsx
- [X] T019 [P] Create ChatMessage component in frontend/components/chat/ChatMessage.tsx
- [X] T020 Mount ChatWidget in frontend/app/layout.tsx

### Agent Setup

- [X] T021 Create OpenAI Agent skeleton with system instructions in backend/agent/todo_agent.py
- [X] T022 Create agent runner utility in backend/agent/runner.py

**Checkpoint**: Foundation ready - chat UI visible, API responds, agent initialized (no tools yet)

---

## Phase 3: User Story 1 - Add Task via Natural Language (P1) 🎯 MVP

**Goal**: Users can add tasks by typing "add buy groceries" or "remember to call mom"

**Independent Test**: Send "add buy milk" → verify task created in database with title "buy milk"

### Tests for US1

- [X] T023 [P] [US1] Unit test for add_task tool in tests/backend/test_tools.py
- [X] T024 [P] [US1] Integration test for add task flow in tests/backend/test_chat_endpoint.py

### Implementation for US1

- [X] T025 [US1] Implement add_task MCP tool in backend/tools/add_task.py
- [X] T026 [US1] Register add_task tool with agent in backend/agent/todo_agent.py
- [X] T027 [US1] Add add_task intent patterns to agent system prompt
- [X] T028 [US1] Implement POST /api/chat endpoint with add_task support in backend/routes/chat.py
- [X] T029 [US1] Add success animation (fade-in + green check) to ChatMessage in frontend/components/chat/ChatMessage.tsx
- [X] T030 [US1] Test add task end-to-end: "add buy groceries" → confirmation message

**Checkpoint**: US1 complete - users can add tasks via chat

---

## Phase 4: User Story 2 - List Tasks with Filters (P1)

**Goal**: Users can view tasks by saying "show my tasks" or "what's pending?"

**Independent Test**: Create 3 tasks → say "show my tasks" → verify all 3 displayed

### Tests for US2

- [ ] T031 [P] [US2] Unit test for list_tasks tool in tests/backend/test_tools.py
- [ ] T032 [P] [US2] Integration test for list tasks flow in tests/backend/test_chat_endpoint.py

### Implementation for US2

- [X] T033 [US2] Implement list_tasks MCP tool with status filter in backend/tools/list_tasks.py
- [X] T034 [US2] Register list_tasks tool with agent in backend/agent/todo_agent.py
- [X] T035 [US2] Add list_tasks intent patterns to agent system prompt
- [X] T036 [US2] Add staggered fade-up animation for task list display in frontend/components/chat/ChatMessage.tsx
- [X] T037 [US2] Test list tasks end-to-end: "show my tasks" → task list displayed

**Checkpoint**: US2 complete - users can list their tasks via chat

---

## Phase 5: User Story 3 - Complete Task by Name or ID (P1)

**Goal**: Users can mark tasks done by saying "done buy groceries" or "complete task 5"

**Independent Test**: Create task → say "done [task name]" → verify task.completed = true

### Tests for US3

- [ ] T038 [P] [US3] Unit test for complete_task tool in tests/backend/test_tools.py
- [ ] T039 [P] [US3] Integration test for complete with chaining in tests/backend/test_chat_endpoint.py

### Implementation for US3

- [X] T040 [US3] Implement complete_task MCP tool in backend/tools/complete_task.py
- [X] T041 [US3] Register complete_task tool with agent in backend/agent/todo_agent.py
- [X] T042 [US3] Add complete_task intent patterns and chaining rules to agent system prompt
- [X] T043 [US3] Implement fuzzy matching logic for task name lookup in backend/tools/base.py
- [X] T044 [US3] Add clarification prompt when multiple matches in agent system prompt
- [ ] T045 [US3] Add strike-through + green checkmark animation in frontend/components/chat/ChatMessage.tsx
- [ ] T046 [US3] Test complete by name: "done buy groceries" → task marked complete
- [ ] T047 [US3] Test complete by ID: "complete task 5" → task marked complete

**Checkpoint**: US3 complete - users can complete tasks via chat with name/ID

---

## Phase 6: User Story 7 - Animated Chat Experience (P1)

**Goal**: Smooth, animated chat interface with typing indicators and feedback animations

**Independent Test**: Perform actions and verify animations occur within 400ms timing

### Implementation for US7

- [X] T048 [P] [US7] Create TypingIndicator component (3 bouncing dots) in frontend/components/chat/TypingIndicator.tsx
- [X] T049 [P] [US7] Create ToolSpinner component in frontend/components/chat/ToolSpinner.tsx
- [X] T050 [US7] Add message slide-in animation (300ms ease-out) in frontend/components/chat/ChatMessage.tsx
- [ ] T051 [US7] Add error animation (red border + shake) in frontend/components/chat/ChatMessage.tsx
- [X] T052 [US7] Implement prefers-reduced-motion support in all chat components
- [X] T053 [US7] Add mobile keyboard handling (chat above keyboard) in frontend/components/chat/ChatWidget.tsx
- [ ] T054 [US7] Test all animations respect 400ms budget

**Checkpoint**: US7 complete - chat has polished animations

---

## Phase 7: User Story 8 - Conversation Persistence (P1)

**Goal**: Conversation history persists across sessions and server restarts

**Independent Test**: Have conversation → restart server → reload page → history visible

### Tests for US8

- [ ] T055 [P] [US8] Integration test for conversation persistence in tests/backend/test_chat_endpoint.py

### Implementation for US8

- [X] T056 [US8] Implement GET /api/chat/history endpoint in backend/routes/chat.py
- [X] T057 [US8] Implement DELETE /api/chat/clear endpoint in backend/routes/chat.py
- [X] T058 [US8] Add conversation get-or-create logic in backend/routes/chat.py
- [X] T059 [US8] Persist user messages to Message table in backend/routes/chat.py
- [X] T060 [US8] Persist assistant messages with tool_calls to Message table in backend/routes/chat.py
- [X] T061 [US8] Load conversation history on chat mount in frontend/hooks/useChat.ts
- [ ] T062 [US8] Test persistence: send messages → restart server → reload page → history intact

**Checkpoint**: US8 complete - stateless server with persistent conversations

---

## Phase 8: User Story 4 - Delete Task (P2)

**Goal**: Users can delete tasks by saying "delete buy groceries" or "remove task 3"

**Independent Test**: Create task → say "delete [task name]" → verify task removed from database

### Tests for US4

- [ ] T063 [P] [US4] Unit test for delete_task tool in tests/backend/test_tools.py

### Implementation for US4

- [X] T064 [US4] Implement delete_task MCP tool in backend/tools/delete_task.py
- [X] T065 [US4] Register delete_task tool with agent in backend/agent/todo_agent.py
- [X] T066 [US4] Add delete_task intent patterns and chaining rules to agent system prompt
- [ ] T067 [US4] Add fade-out + red trash icon animation in frontend/components/chat/ChatMessage.tsx
- [ ] T068 [US4] Test delete by name: "delete old item" → task removed

**Checkpoint**: US4 complete - users can delete tasks via chat

---

## Phase 9: User Story 5 - Update Task (P2)

**Goal**: Users can update tasks by saying "rename task 5 to new title"

**Independent Test**: Create task → say "change [old] to [new]" → verify title updated

### Tests for US5

- [ ] T069 [P] [US5] Unit test for update_task tool in tests/backend/test_tools.py

### Implementation for US5

- [X] T070 [US5] Implement update_task MCP tool in backend/tools/update_task.py
- [X] T071 [US5] Register update_task tool with agent in backend/agent/todo_agent.py
- [X] T072 [US5] Add update_task intent patterns and chaining rules to agent system prompt
- [ ] T073 [US5] Add text highlight + scale-up animation in frontend/components/chat/ChatMessage.tsx
- [ ] T074 [US5] Test update by name: "change buy milk to buy almond milk" → title updated

**Checkpoint**: US5 complete - users can update tasks via chat

---

## Phase 10: User Story 6 - View Profile Information (P3)

**Goal**: Users can ask "who am I?" to see basic account info

**Independent Test**: Say "who am I?" → verify username and created_at displayed (no sensitive data)

### Tests for US6

- [ ] T075 [P] [US6] Unit test for get_user_details tool in tests/backend/test_tools.py

### Implementation for US6

- [X] T076 [US6] Implement get_user_details MCP tool in backend/tools/get_user_details.py
- [X] T077 [US6] Register get_user_details tool with agent in backend/agent/todo_agent.py
- [X] T078 [US6] Add profile intent patterns to agent system prompt
- [ ] T079 [US6] Add profile card slide-in animation in frontend/components/chat/ChatMessage.tsx
- [ ] T080 [US6] Test profile: "who am I?" → username and created_at displayed

**Checkpoint**: US6 complete - users can view basic profile via chat

---

## Phase 11: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T081 [P] Add rate limiting middleware to chat endpoint in backend/routes/chat.py
- [X] T082 [P] Add exponential backoff for OpenAI API calls in backend/agent/runner.py
- [ ] T083 [P] Create manual test scenarios document in specs/001-ai-todo-chatbot/test-scenarios.md
- [ ] T084 Update README.md with Phase III setup instructions
- [ ] T085 [P] Add chat-specific environment variables to documentation
- [ ] T086 Security audit: verify no sensitive data exposure in all tool responses
- [ ] T087 Run full test suite and fix any failures
- [ ] T088 Validate quickstart.md flows work end-to-end

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1: Setup ──────────────────────────────────────────────────┐
                                                                  │
Phase 2: Foundational (BLOCKS all user stories) ◄─────────────────┘
    │
    ├──► Phase 3: US1 Add Task (P1) ──► MVP CHECKPOINT
    │
    ├──► Phase 4: US2 List Tasks (P1) ──┐
    │                                    │
    ├──► Phase 5: US3 Complete Task (P1)─┤──► Core CRUD Complete
    │                                    │
    ├──► Phase 6: US7 Animations (P1) ───┤
    │                                    │
    ├──► Phase 7: US8 Persistence (P1) ──┘
    │
    ├──► Phase 8: US4 Delete Task (P2)
    │
    ├──► Phase 9: US5 Update Task (P2)
    │
    └──► Phase 10: US6 Profile (P3)
                │
                ▼
        Phase 11: Polish
```

### User Story Dependencies

- **US1 (Add Task)**: No dependencies on other stories - can be MVP alone
- **US2 (List Tasks)**: No dependencies - can run in parallel with US1
- **US3 (Complete Task)**: Requires US2 (list_tasks) for chaining by name
- **US4 (Delete Task)**: Requires US2 (list_tasks) for chaining by name
- **US5 (Update Task)**: Requires US2 (list_tasks) for chaining by name
- **US6 (Profile)**: No dependencies on other stories
- **US7 (Animations)**: No dependencies - can run in parallel
- **US8 (Persistence)**: Should complete early (affects all tool usage)

### Parallel Opportunities

Within each phase, tasks marked [P] can run in parallel:
- All Setup tasks (T001-T006)
- Database models (T007, T008)
- Chat UI shell components (T017-T019)
- Tests within same story
- Animation components (T048, T049)

---

## Parallel Example: Foundational Phase

```bash
# Launch all database models together:
Task: "Create Conversation SQLModel in backend/models/conversation.py"
Task: "Create Message SQLModel in backend/models/message.py"

# Launch all UI shell components together:
Task: "Create ChatWidget container in frontend/components/chat/ChatWidget.tsx"
Task: "Create ChatInput component in frontend/components/chat/ChatInput.tsx"
Task: "Create ChatMessage component in frontend/components/chat/ChatMessage.tsx"
```

---

## Implementation Strategy

### MVP First (US1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (database, basic UI, agent)
3. Complete Phase 3: US1 Add Task
4. **STOP and VALIDATE**: Test "add buy groceries" works end-to-end
5. Deploy/demo if ready - users can add tasks!

### Core CRUD Complete (US1-US3)

1. Complete MVP (US1)
2. Add US2: List Tasks
3. Add US3: Complete Task (with chaining)
4. **STOP and VALIDATE**: Users can add, list, and complete tasks
5. Add US7: Animations polish
6. Add US8: Persistence (critical for production)

### Full Feature (All Stories)

1. Complete Core CRUD + Animations + Persistence
2. Add US4: Delete Task
3. Add US5: Update Task
4. Add US6: Profile
5. Complete Phase 11: Polish

### Suggested Parallel Team Strategy

With 2 developers:
- **Dev A**: US1 → US3 → US4 → US5 (backend tools + chaining)
- **Dev B**: US7 → US8 → US6 (frontend + persistence + profile)

---

## Summary

| Phase | Tasks | Parallel Opportunities |
|-------|-------|------------------------|
| Setup | 6 | 5 parallel |
| Foundational | 16 | 8 parallel |
| US1 Add Task | 8 | 2 parallel |
| US2 List Tasks | 7 | 2 parallel |
| US3 Complete Task | 10 | 2 parallel |
| US7 Animations | 7 | 2 parallel |
| US8 Persistence | 8 | 1 parallel |
| US4 Delete Task | 6 | 1 parallel |
| US5 Update Task | 6 | 1 parallel |
| US6 Profile | 6 | 1 parallel |
| Polish | 8 | 5 parallel |
| **Total** | **88** | **30 parallel** |

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story
- Each user story independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate
- MVP = Phase 1 + 2 + 3 (Setup + Foundational + US1 Add Task)
