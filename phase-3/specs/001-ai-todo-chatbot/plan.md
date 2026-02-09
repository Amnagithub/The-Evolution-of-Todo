# Implementation Plan: AI Todo Chatbot (Phase III)

**Branch**: `001-ai-todo-chatbot` | **Date**: 2026-02-05 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-ai-todo-chatbot/spec.md`

---

## Summary

Natural-language todo management via AI chatbot integrated into the existing Phase II full-stack application. Users interact through a floating chat widget, sending commands like "add buy groceries" or "done report". The system uses MCP tools with an OpenAI Agent to execute operations against the existing task database, with full conversation persistence and animated UI feedback.

**Key integration points**:
- Extends Phase II FastAPI backend with new `/api/chat` endpoint
- Reuses Better Auth session validation (no auth changes)
- Adds Conversation/Message tables to existing Neon PostgreSQL
- Mounts animated chat widget in Phase II Next.js frontend

---

## Technical Context

**Language/Version**: Python 3.11 (backend), TypeScript/Next.js 14 (frontend)
**Primary Dependencies**: FastAPI 0.109, SQLModel 0.0.14, OpenAI SDK ^1.6, MCP SDK ^0.9, Framer Motion ^11
**Storage**: Neon PostgreSQL (existing Phase II database, extended)
**Testing**: pytest (backend), manual E2E (frontend)
**Target Platform**: Web application (desktop + mobile browsers)
**Project Type**: Web (frontend + backend monorepo)
**Performance Goals**: <3s task creation, <400ms animations, 100 concurrent users
**Constraints**: Stateless server, prefers-reduced-motion support, no sensitive data exposure
**Scale/Scope**: Single-user conversations, ~50 messages per session typical

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Evidence |
|-----------|--------|----------|
| **I. No Human Code** | PASS | All implementation via Claude Code |
| **II. AI-Generated Code** | PASS | Claude Code is sole implementation agent |
| **III. Spec-Derived Outputs** | PASS | All code derived from this spec |
| **IV. Agent Boundaries** | PASS | Agents write specs/plans, Claude Code implements |
| **V. Phase Isolation** | PASS | Phase III extends Phase II, no Phase IV concepts |
| **VI. Spec Authority** | PASS | Spec.md is source of truth |

**Workflow compliance**: sp.specify → sp.plan (this) → sp.tasks → Claude Code → Review

---

## Project Structure

### Documentation (this feature)

```text
specs/001-ai-todo-chatbot/
├── spec.md              # Feature specification
├── plan.md              # This file (implementation plan)
├── research.md          # Phase 0 research findings
├── data-model.md        # Entity definitions
├── quickstart.md        # Setup guide
├── contracts/
│   ├── chat-api.yaml    # OpenAPI specification
│   └── mcp-tools.json   # MCP tool schemas
├── checklists/
│   └── requirements.md  # Spec quality checklist
└── tasks.md             # Implementation tasks (created by /sp.tasks)
```

### Source Code (repository root)

```text
backend/
├── main.py                    # Modified: add chat router
├── database.py                # Existing (no changes)
├── models/
│   ├── task.py               # Existing (no changes)
│   ├── conversation.py       # NEW: Conversation SQLModel
│   └── message.py            # NEW: Message SQLModel
├── routes/
│   ├── tasks.py              # Existing (no changes)
│   └── chat.py               # NEW: Chat endpoints
├── tools/                     # NEW: MCP tool implementations
│   ├── __init__.py
│   ├── base.py               # Tool base class + context
│   ├── add_task.py
│   ├── list_tasks.py
│   ├── complete_task.py
│   ├── delete_task.py
│   ├── update_task.py
│   └── get_user_details.py
├── agent/                     # NEW: AI agent
│   ├── __init__.py
│   └── todo_agent.py         # OpenAI Agent setup + instructions
├── middleware/
│   └── jwt_auth.py           # Existing (reused for chat)
└── requirements.txt           # Modified: add openai, mcp

frontend/
├── app/
│   └── layout.tsx            # Modified: mount ChatWidget
├── components/
│   ├── chat/                  # NEW: Chat components
│   │   ├── ChatWidget.tsx    # Floating widget container
│   │   ├── ChatMessage.tsx   # Message bubble with animations
│   │   ├── ChatInput.tsx     # Input field with send button
│   │   ├── TypingIndicator.tsx # Bouncing dots
│   │   ├── ToolSpinner.tsx   # Tool call indicator
│   │   └── index.ts          # Exports
│   └── ...existing
├── lib/
│   ├── chat-api.ts           # NEW: Chat API client
│   └── ...existing
├── hooks/
│   └── useChat.ts            # NEW: Chat state management
└── package.json              # Modified: add framer-motion

tests/
├── backend/
│   ├── test_tools.py         # Unit tests for MCP tools
│   ├── test_chat_endpoint.py # Integration tests
│   └── test_agent.py         # Agent behavior tests
└── frontend/
    └── (manual test scenarios)
```

**Structure Decision**: Web application structure extending existing Phase II layout. New code added in dedicated directories (`tools/`, `agent/`, `components/chat/`) to minimize merge conflicts.

---

## Implementation Phases

### Phase A: Preparation & Compatibility Check

**Dependencies**: None
**Risks**:
- Database schema conflicts with Phase II migrations
- Better Auth middleware/dependency version mismatch
- Frontend design system/tailwind/animation library conflicts

**Deliverables**:
- [x] Compatibility report (in research.md)
- [x] Decision log (reused vs extended vs new components)
- [ ] Updated .env.example with OPENAI_API_KEY

**Outcome**: research.md confirms full compatibility with Phase II stack.

---

### Phase B: Database & Models

**Dependencies**: Phase A
**Risks**:
- Migration conflicts with live data
- Missing user fields for get_user_details

**Deliverables**:
- [ ] SQLModel classes: Conversation, Message
- [ ] Alembic migration script
- [ ] Model unit tests

**Key decisions**:
- One conversation per user (UNIQUE constraint on user_id)
- Messages cascade delete with conversation
- tool_calls stored as JSONB

---

### Phase C: MCP Tools

**Dependencies**: Phase B
**Risks**:
- Better Auth current_user injection not working in MCP context
- Tool schema mismatches with OpenAI Agents SDK

**Deliverables**:
- [ ] 6 MCP tool implementations (add, list, complete, delete, update, get_user_details)
- [ ] Ownership checks + error responses on all tools
- [ ] Tool unit tests with mocked database

**Key decisions**:
- Tools receive user_id from endpoint context (not from tool arguments)
- All tools return consistent response shape
- Error messages follow spec templates

---

### Phase D: Agent + Stateless Chat Logic

**Dependencies**: Phase C
**Risks**:
- Poor tool calling reliability (temperature, prompt clarity)
- Conversation history race conditions

**Deliverables**:
- [ ] OpenAI Agent with all 6 tools + dense behavior instructions
- [ ] Stateless POST /api/chat endpoint
- [ ] GET /api/chat/history endpoint
- [ ] DELETE /api/chat/clear endpoint
- [ ] Integration tests for chat flow

**Key decisions**:
- Temperature = 0.3 for consistent tool calling
- Fuzzy match threshold = 0.6 similarity
- Single conversation per user (get-or-create pattern)

---

### Phase E: Frontend ChatKit + Animations

**Dependencies**: Phase D
**Risks**:
- Animation performance on low-end mobile
- Z-index/layout shift conflicts with Phase II UI

**Deliverables**:
- [ ] ChatWidget component (floating, collapsible)
- [ ] ChatMessage component with role-based styling
- [ ] Typing indicator (3 bouncing dots)
- [ ] Tool spinner
- [ ] Success/error animations
- [ ] prefers-reduced-motion support
- [ ] Mobile keyboard handling

**Key decisions**:
- Framer Motion for enter/exit animations
- CSS keyframes for infinite loops (typing dots)
- Fixed position bottom-right, z-index: 50

---

### Phase F: Testing & Hardening

**Dependencies**: Phase E
**Risks**:
- Missed edge cases (chaining failures, concurrent requests)
- Animation accessibility regressions

**Deliverables**:
- [ ] pytest suite: tools + endpoint + chaining
- [ ] Manual test scenarios document
- [ ] Basic rate limiting on chat endpoint

**Key test scenarios**:
- Tool chaining (complete task by name)
- Multiple fuzzy matches (clarification prompt)
- Unauthorized access attempts
- Session expiry handling

---

### Phase G: Documentation & Handover

**Dependencies**: Phase F
**Risks**:
- Incomplete setup instructions → deployment failure

**Deliverables**:
- [ ] Updated README.md (setup, migrations, env vars)
- [ ] Tool JSON schemas in /specs
- [ ] Final repo structure delta vs Phase II

---

## Complexity Tracking

> No violations detected. All complexity justified by spec requirements.

| Aspect | Complexity | Justification |
|--------|------------|---------------|
| 6 MCP tools | Medium | Spec requires full CRUD + user details |
| Conversation persistence | Medium | Spec requires stateless server |
| Animated UI | Medium | Spec requires 6 distinct animations |
| Agent behavior rules | High | Spec requires chaining + clarification |

---

## Dependencies Summary

| New Dependency | Version | Purpose |
|----------------|---------|---------|
| openai | ^1.6.0 | Agent SDK + API |
| mcp | ^0.9.0 | Tool definitions |
| framer-motion | ^11.0.0 | React animations |

---

## Risk Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| OpenAI API rate limits | Low | High | Implement exponential backoff |
| Tool calling errors | Medium | Medium | Dense system prompt + 0.3 temperature |
| Animation jank | Medium | Low | GPU-accelerated transforms only |
| Session expiry mid-chat | Low | Medium | Graceful error + re-auth prompt |

---

## Next Steps

1. Run `/sp.tasks` to generate detailed implementation task list
2. Begin implementation with Phase B (database models)
3. Focus on Phase C (MCP tools) as critical path
4. Phase E (frontend) can partially parallel Phase D

---

## Artifacts Generated

| Artifact | Path | Status |
|----------|------|--------|
| Spec | specs/001-ai-todo-chatbot/spec.md | Complete |
| Plan | specs/001-ai-todo-chatbot/plan.md | Complete |
| Research | specs/001-ai-todo-chatbot/research.md | Complete |
| Data Model | specs/001-ai-todo-chatbot/data-model.md | Complete |
| Quickstart | specs/001-ai-todo-chatbot/quickstart.md | Complete |
| Chat API Contract | specs/001-ai-todo-chatbot/contracts/chat-api.yaml | Complete |
| MCP Tools Schema | specs/001-ai-todo-chatbot/contracts/mcp-tools.json | Complete |
| Requirements Checklist | specs/001-ai-todo-chatbot/checklists/requirements.md | Complete |
| Tasks | specs/001-ai-todo-chatbot/tasks.md | Pending (/sp.tasks) |
