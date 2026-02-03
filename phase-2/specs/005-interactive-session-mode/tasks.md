# Tasks: Interactive Session Mode

**Feature**: 005-interactive-session-mode
**Input**: Design documents from `specs/005-interactive-session-mode/` (plan.md, spec.md, research.md)
**Tests**: NOT requested in spec - tests are optional

**Organization**: Tasks grouped by implementation phase

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

---

## Phase 1: Interactive Session Implementation

**Purpose**: Implement interactive session mode by modifying main.py only

**Single File Modified**: `phase-1/source/todo/cli/main.py`

- [X] T001 [US1] Add interactive mode detection with `sys.argv[1:]` empty check
- [X] T002 [US1] Create `_start_interactive_session()` function for session loop
- [X] T003 [US1] Add single TaskService instance creation before loop
- [X] T004 [US1] Implement session loop with `> ` prompt display
- [X] T005 [US1] Add line reading from stdin using `sys.stdin.readline()`
- [X] T006 [US1] Implement exit handling for "exit" and "quit" commands
- [X] T007 [US1] Add empty line handling (skip with continue)
- [X] T008 [US1] Add `shlex.split()` for parsing quoted arguments
- [X] T009 [US1] Create ArgumentParser and parse command-line arguments
- [X] T010 [US1] Retrieve command instance from subparsers registry
- [X] T011 [US1] Execute command with shared TaskService instance
- [X] T012 [US1] Add error handling for unrecognized commands
- [X] T013 [US1] Add welcome message on session start

**Checkpoint**: Interactive session mode is fully functional

---

## Phase 2: Backward Compatibility Verification

**Purpose**: Ensure non-interactive commands still work as before

- [X] T014 Verify `todo add "task"` still works with arguments
- [X] T015 Verify all other commands (list, complete, etc.) work non-interactively
- [X] T016 Verify non-interactive mode remains stateless (each invocation is independent)

**Checkpoint**: Backward compatibility confirmed

---

## Phase 3: Edge Cases & Polish

**Purpose**: Handle edge cases identified in spec

- [X] T017 Handle empty line input (just pressing Enter)
- [X] T018 Handle unrecognized commands with user-friendly error message
- [X] T019 Handle Ctrl+C (SIGINT) gracefully - exit session on interrupt
- [X] T020 Add proper line stripping for user input

**Checkpoint**: Edge cases handled

---

## Dependencies & Execution Order

### Phase Dependencies

| Phase | Depends On | Blocks |
|-------|-----------|--------|
| Phase 1: Implementation | None | Phases 2-3 |
| Phase 2: Compatibility | Phase 1 | None |
| Phase 3: Edge Cases | Phase 1 | None |

### User Story Dependencies

| Story | Depends On | Can Start After |
|-------|-----------|-----------------|
| US1 (Session Entry) | Plan, Research | Phase 1 |
| US2 (State Persistence) | Plan, Research | Phase 1 (all tasks share main.py) |
| US3 (Session Exit) | Plan, Research | Phase 1 |
| US4 (Syntax Consistency) | Plan, Research | Phase 1 |

### Critical Path (MVP)

1. Phase 1: Complete all implementation tasks (T001-T013)
2. **STOP**: Test interactive session works
3. Phase 2: Verify backward compatibility
4. Phase 3: Handle edge cases

---

## Parallel Opportunities

All tasks within Phase 1 are sequential (same file - main.py). No parallel execution possible.

After Phase 1, Phases 2 and 3 can run in parallel since they are verification and polish tasks.

---

## Implementation Strategy

### MVP First (Interactive Session)

1. Complete Phase 1: Interactive session implementation
2. **STOP and VALIDATE**: Test `uv run todo` enters session, commands persist state
3. Demo: Interactive workflow with multiple commands

### Incremental Delivery

1. Complete Phase 1 → Interactive session works
2. Add Phase 2 → Backward compatibility verified
3. Add Phase 3 → Edge cases handled

---

## Task Summary

| Phase | Tasks | Focus |
|-------|-------|-------|
| Phase 1: Implementation | T001-T013 | Main.py modification |
| Phase 2: Compatibility | T014-T016 | Verification |
| Phase 3: Edge Cases | T017-T020 | Polish |
| **Total** | **20 tasks** | |

---

## Notes

- **[P]** marker: Not applicable - all tasks modify the same file (main.py)
- **[Story] labels**: All Phase 1 tasks map to US1 (core session functionality), US2 (persistence), US3 (exit), US4 (consistency)
- Each phase should be independently testable
- Stop at Phase 1 checkpoint to validate interactive session works
- Avoid: multiple files, complex dependencies, Phase II+ concepts
