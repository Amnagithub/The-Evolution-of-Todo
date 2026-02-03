# Implementation Plan: Interactive Session Mode

**Branch**: `005-interactive-session-mode` | **Date**: 2026-01-02 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/sp.specify` and user requirement to "reuse Intermediate-level command handlers"

## Summary

Implement an interactive session mode for the Phase I Todo CLI that:
1. Enters interactive mode when run without arguments (`uv run todo`)
2. Maintains a shared in-memory TaskService instance across all commands in the session
3. Reuses existing command handlers (add, list, search, filter, sort, complete, incomplete, update, delete, help)
4. Exits on `exit` or `quit` commands
5. Displays `> ` prompt for each command

The feature extends the existing CLI without modifying command logic - only the command invocation pattern changes.

## Technical Context

**Language/Version**: Python 3.11+ (existing project uses 3.12)
**Primary Dependencies**: argparse (stdlib), no new dependencies required
**Storage**: In-memory (existing InMemoryTaskRepository, reused for session lifetime)
**Testing**: pytest (existing test infrastructure)
**Target Platform**: Linux/macOS/Windows CLI
**Project Type**: Single Python CLI application
**Performance Goals**: <10ms per command input processing (negligible overhead)
**Constraints**: No file system I/O in interactive mode; single-threaded, synchronous execution
**Scale/Scope**: Single-user session with O(n) task storage where n = tasks per session

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Check | Status | Notes |
|-------|--------|-------|
| Phase I Constraints | ✅ PASS | CLI + in-memory only, no Phase II+ concepts |
| No Human Code | ✅ PASS | Planning phase only, implementation via /sp.tasks |
| Spec-Derived Outputs | ✅ PASS | Plan derived from approved spec.md |
| Phase Isolation | ✅ PASS | No persistence across sessions |
| Agent Boundaries | ✅ PASS | Planning only, no implementation code |

**Phase 1 Re-check (Post-Design)**: ✅ PASS
- No new dependencies introduced
- Structure remains Phase I compliant (CLI + in-memory only)
- Single file modification (main.py) aligns with minimal scope

## Project Structure

### Documentation (this feature)

```text
specs/005-interactive-session-mode/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # N/A - no unknowns to resolve
├── data-model.md        # N/A - reuses existing Task entity
├── quickstart.md        # TBD in Phase 2
├── contracts/           # N/A - CLI, no API contracts
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (Phase 1 - extends existing structure)

```text
phase-1/source/todo/
├── __init__.py
├── domain/
│   ├── __init__.py
│   ├── entities.py          # Task entity (existing, unchanged)
│   ├── value_objects.py     # Priority, TaskStatus (existing, unchanged)
│   ├── repository.py        # InMemoryTaskRepository (existing, unchanged)
│   └── errors.py            # TaskNotFoundError, ValidationError (existing)
├── services/
│   ├── __init__.py
│   └── task_service.py      # TaskService (existing, unchanged)
└── cli/
    ├── __init__.py
    ├── main.py              # MODIFY: Add interactive session loop
    └── commands/
        ├── __init__.py
        ├── base.py          # Command base class (existing)
        ├── add.py           # REUSE (existing)
        ├── list.py          # REUSE (existing)
        ├── search.py        # REUSE (existing)
        ├── filter.py        # REUSE (existing)
        ├── sort.py          # REUSE (existing)
        ├── complete.py      # REUSE (existing)
        ├── incomplete.py    # REUSE (existing)
        ├── update.py        # REUSE (existing)
        ├── delete.py        # REUSE (existing)
        └── help.py          # REUSE (existing)
```

**Structure Decision**: Feature adds interactive mode by modifying only `main.py`. All command handlers remain unchanged. The session loop parses each input line and delegates to existing command execute methods.

## Complexity Tracking

> **Not applicable** - No Constitution Check violations to justify. Feature follows all principles with minimal scope.

## Phase 0: Research

**Status**: Not required - all technical decisions are clear from existing codebase and spec.

| Question | Answer |
|----------|--------|
| How to detect interactive vs non-interactive mode? | Check `len(sys.argv) == 1` (no arguments after program name) |
| How to reuse ArgumentParser for individual lines? | Create parser per iteration, use `shlex.split()` to parse quoted arguments |
| How to share state across commands? | Create single `TaskService(repo)` instance before loop, pass to each command |
| How to handle empty lines? | Skip with continue (no-op) |
| How to handle unrecognized commands? | Print error message, continue loop |

## Phase 1: Design

### Data Model

**No changes required** - Feature reuses existing `Task` entity, `InMemoryTaskRepository`, and `TaskService` without modification.

### Session Loop Flow

```
main()
├── Check if interactive mode (sys.argv[1:] is empty)
├── If interactive:
│   ├── Create single repo instance
│   ├── Create single service instance
│   ├── Print welcome message
│   └── Enter loop:
│       ├── Print "> " prompt
│       ├── Read line from stdin
│       ├── Strip whitespace
│       ├── If "exit" or "quit": break loop
│       ├── If empty line: continue
│       ├── Parse line into arguments (shlex.split)
│       ├── Create ArgumentParser, add subparsers
│       ├── Parse arguments
│       ├── Get command instance from registry
│       ├── Execute command with service
│       └── Continue loop
└── If non-interactive:
    └── Execute single command (existing behavior)
```

### Command Execution in Session

Each existing command already accepts `(args: Namespace, service: TaskService)` signature. The session loop:
1. Creates arguments namespace via argparse parsing of the line
2. Retrieves the command instance from the command registry
3. Calls `command.execute(args, service)` with the shared service instance

### Key Files Modified

| File | Change |
|------|--------|
| `phase-1/source/todo/cli/main.py` | Add interactive session loop with entry condition check |

### Files Unchanged

All other files remain identical - feature extends behavior without modifying existing command logic.

## Phase 2: Contracts & Quickstart

**Contracts**: Not applicable - CLI interface, no external API contracts.

**Quickstart**: Defer to `/sp.tasks` phase for development workflow documentation.

## Open Questions for Implementation

None - all technical decisions resolved from spec and existing codebase patterns.

## Next Steps

1. Run `/sp.tasks` to generate ordered implementation tasks
2. Execute tasks via Claude Code (`/sp.implement` or equivalent)
3. Validate interactive mode preserves state across commands
4. Verify backward compatibility with non-interactive mode
