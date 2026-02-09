---
id: 002
title: Create AI Chatbot Implementation Plan
stage: plan
date: 2026-02-05
surface: agent
model: claude-opus-4-5-20251101
feature: 001-ai-todo-chatbot
branch: 001-ai-todo-chatbot
user: TLS
command: /sp.plan
labels: ["phase3", "planning", "mcp-tools", "architecture", "integration"]
links:
  spec: specs/001-ai-todo-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-ai-todo-chatbot/plan.md
  - specs/001-ai-todo-chatbot/research.md
  - specs/001-ai-todo-chatbot/data-model.md
  - specs/001-ai-todo-chatbot/quickstart.md
  - specs/001-ai-todo-chatbot/contracts/chat-api.yaml
  - specs/001-ai-todo-chatbot/contracts/mcp-tools.json
tests:
  - null
---

## Prompt

Phase III: Todo AI Chatbot
(Integration into existing Phase II full-stack web application)

Phased Plan (5–7 phases):
- Phase A: Preparation & Compatibility Check
- Phase B: Database & Models
- Phase C: MCP Server & Tools
- Phase D: Agent + Stateless Chat Logic
- Phase E: Frontend ChatKit + Animations
- Phase F: Testing & Hardening
- Phase G: Documentation & Handover

Task List (18 representative tasks):
1. Create Phase III compatibility & decision report
2. Define SQLModel classes for new entities
3. Generate & review initial Alembic migration
4. Implement add_task MCP tool
5. Implement list_tasks with status filter
6. Implement get_user_details (safe profile read)
7. Create OpenAI Agent with all 6 tools + behavior instructions
8. Implement stateless /api/{user_id}/chat endpoint
9. Mount ChatKit component in Phase II frontend
10. Add core animations to chat UI

Next realistic steps:
- Start with tasks 1-4 (preparation + database)
- Focus on tasks 6-10 (MCP tools - most critical logic)
- Prioritize frontend animation & ChatKit mounting

## Response snapshot

Created comprehensive implementation plan for Phase III AI Todo Chatbot with 7 artifacts:

**Branch**: `001-ai-todo-chatbot`

**Artifacts Generated**:
1. `plan.md` - Full implementation plan with 7 phases (A-G)
2. `research.md` - Technical research resolving all unknowns
3. `data-model.md` - Entity definitions (Conversation, Message + existing)
4. `quickstart.md` - Setup guide with environment variables
5. `contracts/chat-api.yaml` - OpenAPI specification for chat endpoints
6. `contracts/mcp-tools.json` - MCP tool schemas with security rules

**Key Technical Decisions**:
- Custom chat component (not ChatKit) to avoid domain allowlisting delays
- Framer Motion + CSS keyframes for animations
- One conversation per user (UNIQUE constraint)
- Temperature 0.3 for consistent tool calling
- Fuzzy match threshold 0.6 for task name matching

**Constitution Check**: All 6 principles PASS

**Phase II Integration Points**:
- Reuses Better Auth session validation
- Extends existing Neon PostgreSQL database
- Mounts in Phase II Next.js layout

## Outcome

- Impact: Complete architecture plan for Phase III integration into Phase II app
- Tests: N/A (planning phase)
- Files: 6 new files created in specs/001-ai-todo-chatbot/
- Next prompts: /sp.tasks to generate implementation task list
- Reflection: User-provided phased plan guided structure; research validated Phase II compatibility

## Evaluation notes (flywheel)

- Failure modes observed: None - research confirmed full compatibility
- Graders run and results (PASS/FAIL): Constitution check PASS (6/6 principles)
- Prompt variant (if applicable): Standard /sp.plan flow with user-provided phase structure
- Next experiment (smallest change to try): Proceed to /sp.tasks for task decomposition
