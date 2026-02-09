# Implementation Plan: Phase II - Full-Stack Todo Web Application

**Branch**: `006-fullstack-todo` | **Date**: 2026-01-15 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/006-fullstack-todo/spec.md`

## Summary

Transform the Phase I console todo app into a multi-user web application with full CRUD persistence and JWT-based authentication for user isolation. The system uses a monorepo structure with Next.js 14+ frontend (Better Auth for JWT), FastAPI backend (SQLModel ORM), and Neon Postgres database. All task operations are filtered by authenticated user_id extracted from JWT tokens in the Authorization header.

## Technical Context

**Language/Version**: Python 3.11+ (backend), TypeScript 5.x (frontend)
**Primary Dependencies**: FastAPI, SQLModel, PyJWT (backend); Next.js 14+, Better Auth (frontend)
**Storage**: Neon Postgres with tasks.user_id foreign key and indexes
**Testing**: pytest (backend), Jest/Vitest (frontend), curl for API validation
**Target Platform**: Docker containers (frontend:3000, backend:8000)
**Project Type**: Web application (frontend + backend monorepo)
**Performance Goals**: 100 concurrent authenticated users, <2s auth response
**Constraints**: JWT shared secret via env var, no path-based user_id, header-only auth
**Scale/Scope**: Multi-user task management, 6 API endpoints, responsive desktop UI

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. No Human Code | ✅ PASS | All implementation via Claude Code agents |
| II. AI-Generated Code | ✅ PASS | Claude Code is sole implementation agent |
| III. Spec-Derived Outputs | ✅ PASS | spec.md approved, plan.md in progress |
| IV. Agent Boundaries | ✅ PASS | Using spec-planner → feature-implementer → qa-reviewer |
| V. Phase Isolation | ✅ PASS | Phase II (Web+DB) per constitution table |
| VI. Spec Authority | ✅ PASS | This plan derives from spec.md |

**Phase Constraint Check**: Phase II allows Flask/FastAPI + SQLite/PostgreSQL per constitution. Using FastAPI + Neon Postgres is compliant.

## Project Structure

### Documentation (this feature)

```text
specs/006-fullstack-todo/
├── spec.md              # Feature specification (completed)
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (OpenAPI specs)
│   └── openapi.yaml
├── checklists/          # Quality validation
│   └── requirements.md
└── tasks.md             # Phase 2 output (via /sp.tasks)
```

### Source Code (repository root)

```text
backend/
├── main.py              # FastAPI app entry point
├── models/
│   └── task.py          # SQLModel Task model
├── routes/
│   └── tasks.py         # CRUD endpoints
├── middleware/
│   └── jwt_auth.py      # JWT verification middleware
├── database.py          # Neon Postgres connection
├── requirements.txt     # Python dependencies
└── tests/
    ├── test_tasks.py    # API endpoint tests
    └── test_auth.py     # JWT validation tests

frontend/
├── app/                 # Next.js App Router
│   ├── layout.tsx       # Root layout with auth provider
│   ├── page.tsx         # Landing/redirect page
│   ├── signin/
│   │   └── page.tsx     # Sign in page
│   ├── signup/
│   │   └── page.tsx     # Sign up page
│   └── tasks/
│       └── page.tsx     # Task list/CRUD page
├── lib/
│   ├── api.ts           # API client with auth headers
│   └── auth.ts          # Better Auth configuration
├── components/
│   ├── TaskList.tsx     # Task list component
│   ├── TaskForm.tsx     # Create/edit task form
│   └── AuthGuard.tsx    # Route protection component
├── package.json
└── tests/
    └── components/      # Component tests

docker-compose.yml       # Orchestrates frontend:3000 + backend:8000
.env.example             # Environment variable template
```

**Structure Decision**: Web application structure selected per constitution Phase II constraints. Monorepo with separate frontend/ and backend/ directories, coordinated via docker-compose.yml.

## Architecture Overview

```text
Project Architecture
├── docker-compose.yml
│   ├── up ──► Frontend: Next.js 14+
│   │             └── Better Auth (JWT)
│   │                   └── API Client (/lib/api.ts)
│   │                                 └── calls ──►
│   └── up ──► Backend: FastAPI
│                   └── /api/tasks/*
│                         └── JWT Middleware
│                               └── extracts → user_id
│                                     └── SQLModel ORM
│                                           └── connects to
│                                                 └── Neon Postgres
│                                                       ├── users table (Better Auth)
│                                                       └── tasks table
└── Spec-Kit
    └── /specs/006-fullstack-todo/...
```

## Key Architectural Decisions

| Decision | Options Considered | Chosen | Rationale |
|----------|-------------------|--------|-----------|
| API Paths | `/api/{user_id}/tasks` vs `/api/tasks` (auth) | `/api/tasks` | Stateless JWT provides secure user isolation without exposing user_id in URL; simpler, more secure |
| Authentication | Session DB vs JWT | JWT | Independent frontend/backend verification; no shared session DB needed; Better Auth handles token lifecycle |
| ORM | SQLAlchemy vs SQLModel | SQLModel | Native Pydantic integration with FastAPI; cleaner request/response models; sufficient for CRUD operations |
| Frontend Router | Pages Router vs App Router | App Router | Modern React Server Components; better performance; recommended for new Next.js projects |

## Development Approach

**Methodology**: Agentic concurrent (spec-write → impl → review)

**Agent Chain**:
1. **spec-planner**: Generate specs and implementation plan
2. **feature-implementer**: Execute implementation from specs
3. **qa-reviewer**: Validate security, auth, and user isolation

**Phase Organization**:
1. Spec Phase: write-spec skill → feature specs
2. Plan/Tasks Phase: spec-planner → plan.md, tasks.md
3. Implementation Phase: implement-crud + verify-auth skills
4. Review Phase: qa-reviewer checklist validation

## Testing Strategy

### API Testing (curl with JWT)
```bash
# 200: Own tasks returned
curl -H "Authorization: Bearer <valid_jwt>" http://localhost:8000/api/tasks

# 401: Invalid/missing token
curl -H "Authorization: Bearer invalid" http://localhost:8000/api/tasks

# 201: Task created
curl -X POST -H "Authorization: Bearer <valid_jwt>" \
     -H "Content-Type: application/json" \
     -d '{"title":"Test task"}' \
     http://localhost:8000/api/tasks
```

### UI Testing (Browser)
1. Signup → verify account created
2. Add task → verify appears in list
3. Toggle complete → verify status changes
4. Delete task → verify removed from list
5. Logout → verify session cleared
6. Login as different user → verify no data leak

### Database Validation
```sql
-- Verify user isolation
SELECT * FROM tasks WHERE user_id = 'testuser1';
-- Should return only testuser1's tasks
```

### Full Integration
- `docker-compose up` starts both services
- `docker-compose logs` shows no errors
- `npm run build` succeeds in frontend
- All API endpoints respond correctly

## Complexity Tracking

> No constitution violations requiring justification.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A |

## Next Steps

1. **Phase 0**: research.md - Document technology research and best practices
2. **Phase 1**: data-model.md - Define Task entity schema
3. **Phase 1**: contracts/openapi.yaml - API contract specification
4. **Phase 1**: quickstart.md - Developer setup guide
5. **Phase 2**: tasks.md - Implementation task breakdown (via /sp.tasks)
