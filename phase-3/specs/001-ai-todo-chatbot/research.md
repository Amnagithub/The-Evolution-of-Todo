# Research: AI Todo Chatbot (Phase III)

**Branch**: `001-ai-todo-chatbot`
**Date**: 2026-02-05
**Status**: Complete

---

## Phase II Compatibility Analysis

### Decision: Phase II Integration Strategy

**Decision**: Extend existing Phase II application rather than create separate service

**Rationale**:
- Phase II already has working Better Auth + session-based authentication
- Task model exists with user_id isolation
- Frontend has established Tailwind design system
- Database connection and models are SQLModel-based (easy to extend)

**Alternatives considered**:
- Separate microservice for chatbot: Rejected due to additional auth complexity and deployment overhead
- Replace Phase II entirely: Rejected as violates backward compatibility requirement

---

## Technical Stack Research

### 1. MCP (Model Context Protocol) SDK

**Decision**: Use official MCP Python SDK for tool definitions

**Rationale**:
- Official SDK provides standardized tool schemas compatible with OpenAI Agents
- Type-safe tool definitions with Pydantic
- Built-in validation and error handling

**Implementation approach**:
- Define tools as Python functions with type hints
- MCP SDK generates JSON schemas automatically
- Tools receive user_id from authenticated context

**Alternatives considered**:
- Manual JSON schema definitions: Rejected for maintenance burden
- Custom tool wrapper: Rejected as MCP SDK is the standard

### 2. OpenAI Agents SDK

**Decision**: Use OpenAI Agents SDK with custom tools

**Rationale**:
- Native tool calling support
- Conversation history management
- Streaming support for typing indicators
- Production-ready reliability

**Implementation approach**:
- Create Agent with 6 MCP tools
- Dense system prompt with behavior rules
- Stateless endpoint that loads/persists conversation history

**Alternatives considered**:
- LangChain agents: Rejected for complexity overhead
- Direct OpenAI API: Rejected as Agents SDK simplifies tool orchestration

### 3. Conversation Persistence

**Decision**: Store conversation in PostgreSQL with SQLModel

**Rationale**:
- Maintains stateless server architecture
- Survives server restarts
- Integrates with existing Phase II database
- User isolation via foreign key relationship

**Data model**:
- `Conversation`: id, user_id, created_at, updated_at
- `Message`: id, conversation_id, role (user/assistant), content, tool_calls (JSON), created_at

**Alternatives considered**:
- Redis for conversation cache: Rejected for persistence requirements
- In-memory storage: Rejected as violates stateless requirement
- File-based storage: Rejected for scalability

### 4. Chat UI Implementation

**Decision**: Custom animated chat component (not ChatKit)

**Rationale**:
- ChatKit requires OpenAI domain allowlisting (deployment delay risk)
- Custom component allows full control over animations
- Integrates seamlessly with existing Tailwind design system
- Better accessibility control for prefers-reduced-motion

**Implementation approach**:
- Bottom-right floating widget with toggle button
- React component with Framer Motion for animations
- WebSocket-style experience via fetch + streaming
- CSS keyframe animations for typing dots, spinner

**Alternatives considered**:
- OpenAI ChatKit: Rejected due to domain allowlisting delay risk
- Third-party chat libraries: Rejected for animation customization needs

### 5. Animation Library

**Decision**: Framer Motion + CSS keyframes

**Rationale**:
- Framer Motion for complex enter/exit animations
- CSS keyframes for simple looping animations (typing dots)
- Built-in support for prefers-reduced-motion
- Small bundle size compared to alternatives

**Specific animations**:
| Animation | Technique | Duration |
|-----------|-----------|----------|
| Message slide-in | Framer Motion | 300ms |
| Typing dots | CSS keyframes | infinite loop |
| Tool spinner | CSS keyframes | infinite loop |
| Success check | Framer Motion | 200ms |
| Error shake | CSS keyframes | 150ms |
| Fade-out | Framer Motion | 200ms |

**Alternatives considered**:
- React Spring: Similar capability but larger bundle
- CSS-only animations: Insufficient for complex orchestration
- GSAP: Overkill for this use case

---

## Integration Points Research

### 1. Better Auth Session Extraction

**Decision**: Reuse existing `get_current_user_id()` middleware pattern

**Rationale**:
- Already implemented and working in Phase II
- Validates session token from Authorization header
- Returns user_id string for all operations

**Integration**:
- Chat endpoint uses same dependency injection
- MCP tools receive user_id from endpoint context
- No auth logic duplication

### 2. Database Extension

**Decision**: Add Conversation and Message tables to existing database

**Rationale**:
- Single database instance for all data
- SQLModel provides consistent ORM approach
- Alembic migrations for schema evolution

**Schema additions**:
```sql
-- Conversation table
CREATE TABLE conversation (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL REFERENCES "user"(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Message table
CREATE TABLE message (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL REFERENCES conversation(id),
    role VARCHAR(20) NOT NULL,  -- 'user' or 'assistant'
    content TEXT NOT NULL,
    tool_calls JSONB,  -- Optional tool call data
    created_at TIMESTAMP DEFAULT NOW()
);
```

### 3. Frontend Integration

**Decision**: Floating widget overlay (non-intrusive to Phase II)

**Rationale**:
- Doesn't disrupt existing task management UI
- Accessible from any page
- Can be collapsed/expanded
- Z-index above all other content

**Integration points**:
- Mount in root layout (frontend/app/layout.tsx)
- Share auth context via existing useSession hook
- API calls through existing api.ts utility

---

## Risk Mitigation Research

### 1. Tool Calling Reliability

**Risk**: Agent may misinterpret natural language commands

**Mitigation**:
- Dense system prompt with explicit intent mappings
- Temperature set to 0.3 for consistency
- Fuzzy matching with similarity threshold (>0.6)
- Clarification prompt when multiple matches

### 2. Conversation Race Conditions

**Risk**: Concurrent requests may corrupt conversation history

**Mitigation**:
- Database-level locking on conversation row during update
- Optimistic concurrency with version field (optional)
- Single conversation per user (simplification)

### 3. Animation Performance

**Risk**: Animations may jank on low-end mobile devices

**Mitigation**:
- Use GPU-accelerated transforms only
- Limit to 60fps animations
- prefers-reduced-motion fallback
- Simple fade-only mode for low-power devices

### 4. Session Expiry Mid-Conversation

**Risk**: User loses context when session expires

**Mitigation**:
- Check session validity before each request
- Graceful error with re-auth prompt
- Conversation persists and resumes after re-auth

---

## Dependencies Verification

| Dependency | Version | Purpose | Compatibility |
|------------|---------|---------|---------------|
| openai | ^1.6 | Agent SDK + API calls | Compatible with Python 3.11 |
| mcp | ^0.9 | MCP tool definitions | Works with OpenAI Agents |
| framer-motion | ^11 | React animations | Compatible with Next.js 14 |
| SQLModel | 0.0.14 | Already in Phase II | No changes needed |
| Better Auth | 1.0.0 | Already in Phase II | No changes needed |
| Tailwind CSS | 3.3 | Already in Phase II | No changes needed |

---

## NEEDS CLARIFICATION Resolutions

| Item | Resolution |
|------|------------|
| Chat UI library | Custom component (not ChatKit) - avoids domain allowlisting |
| Animation library | Framer Motion + CSS keyframes |
| Conversation model | Single conversation per user (simplest approach) |
| Tool temperature | 0.3 for consistent responses |
| Fuzzy match threshold | 0.6 similarity score |

---

## Conclusion

All technical unknowns have been resolved. The integration approach:

1. **Backend**: Extend existing FastAPI app with MCP tools and chat endpoint
2. **Database**: Add Conversation/Message tables via Alembic migration
3. **Agent**: OpenAI Agents SDK with 6 MCP tools and dense behavior instructions
4. **Frontend**: Custom animated chat widget in floating overlay
5. **Auth**: Reuse Better Auth session validation (no changes to auth system)

Ready to proceed to Phase 1: Design & Contracts.
