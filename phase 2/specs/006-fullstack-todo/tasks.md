# Tasks: Phase II - Full-Stack Todo Web Application

**Input**: Design documents from `/specs/006-fullstack-todo/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/openapi.yaml, research.md, quickstart.md

**Tests**: Tests are NOT explicitly requested in the feature specification. Tasks focus on implementation only.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/`, `frontend/` at repository root
- Backend: `backend/main.py`, `backend/models/`, `backend/routes/`, `backend/middleware/`
- Frontend: `frontend/app/`, `frontend/lib/`, `frontend/components/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure for both backend and frontend

- [x] T001 Create monorepo directory structure: `backend/`, `frontend/`, `.env.example`
- [x] T002 [P] Initialize backend Python project with `backend/requirements.txt` (fastapi, sqlmodel, pyjwt, uvicorn, python-dotenv)
- [x] T003 [P] Initialize frontend Next.js 14+ project with App Router in `frontend/`
- [x] T004 [P] Create `docker-compose.yml` with frontend:3000 and backend:8000 services
- [x] T005 [P] Create `.env.example` with DATABASE_URL, BETTER_AUTH_SECRET, NEXT_PUBLIC_API_URL placeholders

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T006 Create `backend/database.py` with Neon Postgres connection using SQLModel engine
- [x] T007 Create `backend/models/__init__.py` and `backend/models/task.py` with Task SQLModel (id, title, description, completed, user_id, timestamps)
- [x] T008 Create `backend/main.py` with FastAPI app, CORS middleware, database initialization
- [x] T009 [P] Create `backend/middleware/__init__.py` package structure
- [x] T010 Create `backend/middleware/jwt_auth.py` with JWT verification extracting user_id from BETTER_AUTH_SECRET
- [x] T011 [P] Create `frontend/lib/auth.ts` with Better Auth server configuration (JWT plugin, Neon adapter)
- [x] T012 [P] Create `frontend/lib/auth-client.ts` with client-side auth hooks
- [x] T013 Create `frontend/app/api/auth/[...all]/route.ts` for Better Auth API routes
- [x] T014 [P] Create `frontend/lib/api.ts` with API client that attaches JWT to Authorization header
- [x] T015 Create `frontend/app/layout.tsx` with auth provider wrapping
- [x] T016 [P] Create `frontend/components/AuthGuard.tsx` for route protection
- [x] T017 [P] Create `backend/Dockerfile` for Python FastAPI container
- [x] T018 [P] Create `frontend/Dockerfile` for Next.js container

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - User Registration and Authentication (Priority: P1) 🎯 MVP

**Goal**: Users can signup, signin, and maintain authenticated sessions via JWT

**Independent Test**: Complete signup flow, signin with credentials, verify JWT stored in localStorage, refresh page and stay logged in

### Implementation for User Story 1

- [x] T019 [US1] Create `frontend/app/signup/page.tsx` with email/password registration form using Better Auth
- [x] T020 [US1] Create `frontend/app/signin/page.tsx` with email/password login form using Better Auth
- [x] T021 [US1] Update `frontend/app/page.tsx` to redirect authenticated users to /tasks, unauthenticated to /signin
- [x] T022 [US1] Add signout functionality to layout or navigation component
- [x] T023 [US1] Verify JWT middleware in `backend/middleware/jwt_auth.py` returns 401 for invalid/missing tokens
- [x] T024 [US1] Add error handling for authentication failures (invalid credentials message without revealing which field)

**Checkpoint**: Users can register, login, logout, and sessions persist via JWT

---

## Phase 4: User Story 2 - Create and View Tasks (Priority: P1) 🎯 MVP

**Goal**: Authenticated users can create tasks and view their own task list (not other users' tasks)

**Independent Test**: Create 3 tasks, verify they appear in list sorted by newest first, login as different user and verify no tasks visible

### Implementation for User Story 2

- [x] T025 [US2] Create `backend/routes/__init__.py` package structure
- [x] T026 [US2] Create `backend/routes/tasks.py` with GET /api/tasks endpoint filtered by user_id from JWT
- [x] T027 [US2] Add POST /api/tasks endpoint in `backend/routes/tasks.py` with title validation (1-200 chars, non-whitespace)
- [x] T028 [US2] Register tasks router in `backend/main.py` with JWT middleware dependency
- [x] T029 [US2] Create `frontend/components/TaskForm.tsx` with title (required) and description (optional) inputs
- [x] T030 [US2] Create `frontend/components/TaskList.tsx` displaying tasks sorted by created_at DESC
- [x] T031 [US2] Create `frontend/app/tasks/page.tsx` combining TaskForm and TaskList, protected by AuthGuard
- [x] T032 [US2] Add loading and error states to task list UI
- [x] T033 [US2] Verify user isolation: API returns only authenticated user's tasks (filter by user_id)

**Checkpoint**: Users can create tasks and view their own task list with complete isolation

---

## Phase 5: User Story 3 - Update Tasks (Priority: P2)

**Goal**: Authenticated users can edit task title/description and toggle completion status

**Independent Test**: Create task, edit title/description, verify changes persist, toggle completed status twice

### Implementation for User Story 3

- [x] T034 [US3] Add PUT /api/tasks/{task_id} endpoint in `backend/routes/tasks.py` with user_id ownership check (return 404 if not owned)
- [x] T035 [US3] Add PATCH /api/tasks/{task_id}/complete endpoint in `backend/routes/tasks.py` to toggle completed status
- [x] T036 [US3] Update `frontend/components/TaskList.tsx` with inline edit capability for title/description
- [x] T037 [US3] Add completion toggle checkbox/button to TaskList.tsx calling PATCH endpoint
- [x] T038 [US3] Add optimistic UI updates for task editing and toggling
- [x] T039 [US3] Verify 404 returned when user attempts to update another user's task

**Checkpoint**: Users can edit and toggle tasks they own

---

## Phase 6: User Story 4 - Delete Tasks (Priority: P2)

**Goal**: Authenticated users can permanently delete tasks they own

**Independent Test**: Create task, delete it, verify removed from list, verify cannot delete other user's task

### Implementation for User Story 4

- [x] T040 [US4] Add DELETE /api/tasks/{task_id} endpoint in `backend/routes/tasks.py` with user_id ownership check
- [x] T041 [US4] Add delete button with confirmation dialog to `frontend/components/TaskList.tsx`
- [x] T042 [US4] Implement optimistic delete UI (remove from list immediately, rollback on error)
- [x] T043 [US4] Verify 404 returned when user attempts to delete another user's task

**Checkpoint**: Users can delete their own tasks with confirmation

---

## Phase 7: User Story 5 - View Individual Task Details (Priority: P3)

**Goal**: Authenticated users can view full details of a specific task by ID

**Independent Test**: Create task with description, retrieve by ID, verify all fields including timestamps display

### Implementation for User Story 5

- [x] T044 [US5] Add GET /api/tasks/{task_id} endpoint in `backend/routes/tasks.py` with user_id ownership check
- [x] T045 [US5] Create `frontend/app/tasks/[id]/page.tsx` with full task detail view (title, description, completed, timestamps)
- [x] T046 [US5] Add navigation from TaskList to individual task detail page
- [x] T047 [US5] Handle 404 when task not found or not owned by user

**Checkpoint**: Users can view full details of individual tasks

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T048 [P] Add /health endpoint to `backend/main.py` (no auth required) returning status and timestamp
- [x] T049 [P] Add Tailwind CSS styling to all frontend components for responsive desktop UI
- [x] T050 [P] Add proper error boundary in `frontend/app/error.tsx`
- [x] T051 [P] Add loading UI in `frontend/app/loading.tsx`
- [x] T052 Verify docker-compose up starts both services without errors
- [x] T053 Verify all 6 API endpoints respond correctly per OpenAPI spec in `specs/006-fullstack-todo/contracts/openapi.yaml`
- [x] T054 Run quickstart.md validation: complete signup → CRUD → logout → verify isolation
- [x] T055 Final security review: no secrets in code, JWT validation on all protected routes, user_id filtering on all task queries

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - US1 (Auth) should complete first as US2-5 depend on authenticated sessions
  - US2-5 can proceed after US1 completion
- **Polish (Phase 8)**: Depends on all desired user stories being complete

### User Story Dependencies

```
Phase 1 (Setup)
    │
    ▼
Phase 2 (Foundational)
    │
    ▼
Phase 3 (US1: Auth) ──────────────────────────┐
    │                                         │
    ▼                                         │
Phase 4 (US2: Create/View) ◄──────────────────┤
    │                                         │
    ├───► Phase 5 (US3: Update) ◄─────────────┤
    │                                         │
    ├───► Phase 6 (US4: Delete) ◄─────────────┤
    │                                         │
    └───► Phase 7 (US5: View Details) ◄───────┘
                     │
                     ▼
              Phase 8 (Polish)
```

### Within Each Phase

- Tasks marked [P] can run in parallel (different files)
- Backend and frontend foundational tasks can run in parallel
- Each user story: Backend endpoint → Frontend UI → Integration

### Parallel Opportunities

**Phase 1 (Setup)**: T002, T003, T004, T005 can all run in parallel

**Phase 2 (Foundational)**:
- Backend: T006 → T007 → T008 → T010 (sequential), T009, T017 parallel
- Frontend: T011, T012, T014, T016, T018 can run in parallel, T013 after T011, T015 after T013

**User Stories**: After US1 completes, US3, US4, US5 can proceed in parallel (all depend on US2's task list infrastructure)

---

## Parallel Example: Foundational Phase

```bash
# Launch backend foundational tasks:
Task T006: "Create backend/database.py with Neon connection"
# Then:
Task T007: "Create backend/models/task.py with SQLModel"
# Then:
Task T008: "Create backend/main.py with FastAPI app"
# Parallel:
Task T009: "Create backend/middleware/__init__.py"
Task T017: "Create backend/Dockerfile"

# Launch frontend foundational tasks in parallel with backend:
Task T011: "Create frontend/lib/auth.ts"
Task T012: "Create frontend/lib/auth-client.ts"
Task T014: "Create frontend/lib/api.ts"
Task T016: "Create frontend/components/AuthGuard.tsx"
Task T018: "Create frontend/Dockerfile"
```

---

## Implementation Strategy

### MVP First (User Story 1 + 2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Authentication)
4. Complete Phase 4: User Story 2 (Create/View Tasks)
5. **STOP and VALIDATE**: Test auth + CRUD independently via quickstart.md
6. Deploy/demo if ready - this is a functional MVP!

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add US1 (Auth) → Test independently → Users can register/login
3. Add US2 (Create/View) → Test independently → Deploy/Demo (MVP!)
4. Add US3 (Update) → Test independently → Deploy/Demo
5. Add US4 (Delete) → Test independently → Deploy/Demo
6. Add US5 (View Details) → Test independently → Deploy/Demo
7. Each story adds value without breaking previous stories

### Task Summary

| Phase | Tasks | Parallel Tasks |
|-------|-------|----------------|
| Setup | 5 (T001-T005) | 4 |
| Foundational | 13 (T006-T018) | 9 |
| US1 (Auth) | 6 (T019-T024) | 0 |
| US2 (Create/View) | 9 (T025-T033) | 0 |
| US3 (Update) | 6 (T034-T039) | 0 |
| US4 (Delete) | 4 (T040-T043) | 0 |
| US5 (View Details) | 4 (T044-T047) | 0 |
| Polish | 8 (T048-T055) | 4 |
| **Total** | **55 tasks** | **17 parallel** |

### MVP Scope (Suggested)

**Minimum**: Phase 1-4 (Setup + Foundational + US1 + US2) = **33 tasks**
- Users can register, login, create tasks, view their tasks
- Complete isolation between users
- Functional web app with authentication

---

## Notes

- [P] tasks = different files, no dependencies on each other
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
