# Tasks: Task Organization Feature

**Feature**: 004-task-organization
**Input**: Design documents from `phase-1/specs/` (plan.md, spec.md, data-model.md, contracts/)
**Tests**: NOT requested in spec - tests are optional

**Organization**: Tasks grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1-US10)
- Include exact file paths in descriptions

---

## Phase 1: Domain Foundation

**Purpose**: Core domain changes that ALL user stories depend on

- [X] T001 Create Priority enum in phase-1/source/todo/domain/value_objects.py
- [X] T002 Update TaskStatus with display_name property in phase-1/source/todo/domain/value_objects.py
- [X] T003 Update Task entity: add priority, tags, updated_at fields in phase-1/source/todo/domain/entities.py
- [X] T004 Add task methods: update_priority, add_tag, remove_tag, has_tag in phase-1/source/todo/domain/entities.py
- [X] T005 Add ValidationError for tags in phase-1/source/todo/domain/errors.py (already exists)

---

## Phase 2: Service Layer

**Purpose**: Business logic layer that CLI commands depend on

- [X] T006 Update create_task() to accept priority and tags in phase-1/source/todo/services/task_service.py
- [X] T007 Update update_task methods to handle priority and tags in phase-1/source/todo/services/task_service.py
- [X] T008 Add search_tasks() method in phase-1/source/todo/services/task_service.py
- [X] T009 Add filter_tasks() method in phase-1/source/todo/services/task_service.py
- [X] T010 Add sort_tasks() method in phase-1/source/todo/services/task_service.py

---

## Phase 3: User Story 1 & 2 - Priority & Tags Creation (US-001, US-002) 🎯 MVP FOUNDATION

**Goal**: Enable creating tasks with priority and tags

**Independent Test**: `todo add "Test task" --priority HIGH --tag work` creates task with correct priority and tag

### Modified Command: Add

- [X] T011 [US1] Update add command arguments: --priority, --tag (repeatable), --description in phase-1/source/todo/cli/commands/add.py
- [X] T012 [US1] Update add command output to show priority and tags in phase-1/source/todo/cli/commands/add.py
- [X] T013 [US1] Add priority and tag validation in add command in phase-1/source/todo/cli/commands/add.py

**Checkpoint**: User can create tasks with priority and tags

---

## Phase 4: User Story 10 - List Display Enhancement (US-010)

**Goal**: Show priority and tags in list output

**Independent Test**: `todo list` shows Priority and Tags columns; `todo list --extended` shows full details

### Modified Command: List

- [X] T014 [US10] Add --extended flag to list command in phase-1/source/todo/cli/commands/list.py
- [X] T015 [US10] Update compact output format with Priority and Tags columns in phase-1/source/todo/cli/commands/list.py
- [X] T016 [US10] Implement extended output format with all fields in phase-1/source/todo/cli/commands/list.py

**Checkpoint**: List displays priority and tags correctly

---

## Phase 5: User Story 1 & 2 - Update Priority & Tags (US-001, US-002)

**Goal**: Enable updating priority and tags on existing tasks

**Independent Test**: `todo update 1 --priority LOW --add-tag new-tag --remove-tag old-tag` updates task correctly

### Modified Command: Update

- [X] T017 [US1] Update update command: add --priority argument in phase-1/source/todo/cli/commands/update.py
- [X] T018 [US2] Update update command: add --add-tag, --remove-tag, --description arguments in phase-1/source/todo/cli/commands/update.py
- [X] T019 [US1] Update update command output to show changed values in phase-1/source/todo/cli/commands/update.py

**Checkpoint**: User can update task priority and tags

---

## Phase 6: User Story 3 - Search Command (US-003)

**Goal**: Search tasks by keyword in title or description

**Independent Test**: `todo search "keyword"` finds matching tasks; `todo search "nonexistent"` reports no results

### New Command: Search

- [X] T020 [US3] Create search command file in phase-1/source/todo/cli/commands/search.py
- [X] T021 [US3] Implement search argument parser with --status, --priority, --tag filters in phase-1/source/todo/cli/commands/search.py
- [X] T022 [US3] Implement search execution using TaskService.search_tasks() in phase-1/source/todo/cli/commands/search.py
- [X] T023 [US3] Implement search output formatter matching contract in phase-1/source/todo/cli/commands/search.py
- [X] T024 [US3] Add search command to main.py subparsers in phase-1/source/todo/cli/main.py

**Checkpoint**: Search command works with all options

---

## Phase 7: User Stories 4, 5, 6 - Filter Command (US-004, US-005, US-006)

**Goal**: Filter tasks by status, priority, and/or tag

**Independent Test**: `todo filter --status ACTIVE --priority HIGH --tag work` shows only matching tasks

### New Command: Filter

- [X] T025 [US4] Create filter command file in phase-1/source/todo/cli/commands/filter.py
- [X] T026 [US5] Implement filter argument parser with --status, --priority, --tag options in phase-1/source/todo/cli/commands/filter.py
- [X] T027 [US6] Implement filter execution using TaskService.filter_tasks() in phase-1/source/todo/cli/commands/filter.py
- [X] T028 [US4] Implement filter output formatter matching contract in phase-1/source/todo/cli/commands/filter.py
- [X] T029 [US4] Add filter command to main.py subparsers in phase-1/source/todo/cli/main.py

**Checkpoint**: Filter command works with all filter combinations

---

## Phase 8: User Stories 7, 8, 9 - Sort Command (US-007, US-008, US-009)

**Goal**: Sort tasks by title, priority, id, or created date

**Independent Test**: `todo sort priority` shows HIGH > MEDIUM > LOW; `todo sort title --reverse` reverses order

### New Command: Sort

- [X] T030 [US7] Create sort command file in phase-1/source/todo/cli/commands/sort.py
- [X] T031 [US8] Implement sort argument parser with field argument and --reverse flag in phase-1/source/todo/cli/commands/sort.py
- [X] T032 [US9] Implement sort execution using TaskService.sort_tasks() in phase-1/source/todo/cli/commands/sort.py
- [X] T033 [US7] Implement sort output formatter matching contract in phase-1/source/todo/cli/commands/sort.py
- [X] T034 [US7] Add sort command to main.py subparsers in phase-1/source/todo/cli/main.py

**Checkpoint**: Sort command works with all fields and reverse option

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Integration and validation across all features

- [X] T035 Update main.py help to include new commands in phase-1/source/todo/cli/main.py
- [X] T036 Test data migration for existing tasks (not applicable - in-memory storage)
- [X] T037 Verify all existing tests still pass in tests/ (0 tests in project)
- [X quickstart.md validation] T038 Run commands in phase-1/specs/quickstart.md

---

## Dependencies & Execution Order

### Phase Dependencies

| Phase | Depends On | Blocks |
|-------|-----------|--------|
| Phase 1: Domain | None | All other phases |
| Phase 2: Service | Phase 1 | Phases 3-8 |
| Phase 3: Add Command | Phase 2 | Independent |
| Phase 4: List Command | Phase 2 | Independent |
| Phase 5: Update Command | Phase 2 | Independent |
| Phase 6: Search Command | Phase 2 | Independent |
| Phase 7: Filter Command | Phase 2 | Independent |
| Phase 8: Sort Command | Phase 2 | Independent |
| Phase 9: Polish | Phases 3-8 | None |

### User Story Dependencies

| Story | Depends On | Can Start After |
|-------|-----------|-----------------|
| US-001 (Priority) | Domain + Service | Phase 2 |
| US-002 (Tags) | Domain + Service | Phase 2 |
| US-003 (Search) | Domain + Service | Phase 2 |
| US-004 (Filter Status) | Domain + Service | Phase 2 |
| US-005 (Filter Priority) | Domain + Service | Phase 2 |
| US-006 (Filter Tag) | Domain + Service | Phase 2 |
| US-007 (Sort Title) | Domain + Service | Phase 2 |
| US-008 (Sort Priority) | Domain + Service | Phase 2 |
| US-009 (Sort Created) | Domain + Service | Phase 2 |
| US-010 (List Display) | Domain | Phase 1 |

### Critical Path (MVP)

1. Phase 1: Domain Foundation
2. Phase 2: Service Layer
3. Phase 3: Add Command (US-001, US-002) - MVP delivers basic priority/tag creation
4. **STOP**: Validate basic functionality works

---

## Parallel Opportunities

Within each phase, tasks marked [P] can run in parallel:

- **Phase 1**: T001, T002, T003 can run in parallel (different files)
- **Phase 2**: T006-T010 can run in parallel (different methods)
- **Phases 3-8**: Each command's sub-tasks can run in parallel within the command file
- **Across phases**: Phases 3-8 are independent of each other and can proceed in parallel once Phase 2 is complete

### Parallel Example: After Phase 2

Once Phase 2 (Service Layer) is complete, the following can run in parallel:
- Developer A: Phase 3 (Add command)
- Developer B: Phase 4 (List command)
- Developer C: Phase 5 (Update command)
- Developer D: Phase 6 (Search command)
- Developer E: Phase 7 (Filter command)
- Developer F: Phase 8 (Sort command)

---

## Implementation Strategy

### MVP First (Priority & Tags Creation)

1. Complete Phase 1: Domain Foundation
2. Complete Phase 2: Service Layer
3. Complete Phase 3: Add Command
4. **Validate**: `todo add "Test" --priority HIGH --tag work` works
5. Demo: Basic priority/tag creation functionality

### Incremental Delivery

1. MVP: Phases 1-3 (Priority/Tag creation via add)
2. Add Phase 4 (List display) → Test → Demo
3. Add Phase 5 (Update priority/tags) → Test → Demo
4. Add Phase 6 (Search) → Test → Demo
5. Add Phase 7 (Filter) → Test → Demo
6. Add Phase 8 (Sort) → Test → Demo
7. Phase 9: Polish

### Parallel Team Strategy

With multiple developers:
1. Team completes Phases 1-2 together (foundation)
2. Once Phase 2 is done, split into pairs:
   - Pair A: Phase 3 (Add) + Phase 5 (Update)
   - Pair B: Phase 4 (List) + Phase 8 (Sort)
   - Pair C: Phase 6 (Search) + Phase 7 (Filter)
3. All phases complete simultaneously

---

## Task Summary

| Phase | Tasks | User Stories |
|-------|-------|--------------|
| Phase 1: Domain | T001-T005 | Foundation |
| Phase 2: Service | T006-T010 | Foundation |
| Phase 3: Add | T011-T013 | US-001, US-002 |
| Phase 4: List | T014-T016 | US-010 |
| Phase 5: Update | T017-T019 | US-001, US-002 |
| Phase 6: Search | T020-T024 | US-003 |
| Phase 7: Filter | T025-T029 | US-004, US-005, US-006 |
| Phase 8: Sort | T030-T034 | US-007, US-008, US-009 |
| Phase 9: Polish | T035-T038 | Cross-cutting |
| **Total** | **38 tasks** | **10 user stories** |

---

## Notes

- [P] tasks = different files, no dependencies - can run in parallel
- [Story] label maps task to specific user story for traceability
- Each phase should be independently testable
- Stop at any checkpoint to validate current work
- Avoid: vague tasks, same file conflicts, cross-story dependencies
- Tests are NOT requested in spec - implementation focuses on functionality only
