# Research: Interactive Session Mode

**Feature**: 005-interactive-session-mode
**Date**: 2026-01-02

## Research Status

**Not Required** - All technical decisions are derivable from the existing codebase and specification without external research.

## Technical Decisions

| Decision | Rationale | Alternatives Considered |
|----------|-----------|------------------------|
| Use `sys.argv[1:]` to detect interactive mode | Reliable cross-platform method; empty list = no arguments | Using `sys.stdin.isatty()` - less reliable, fails in piped input scenarios |
| Use `shlex.split()` for parsing | Handles quoted arguments correctly (`"task name"` → `["task", "name"]`) | `str.split()` - doesn't handle quotes, `argparse.split()` - requires pre-parsing |
| Single ArgumentParser per iteration | Reuses existing command parser definitions without modification | Pre-create all parsers - increases memory, parser state issues |
| Single service instance per session | Provides shared in-memory repository across all commands | Create new service per command - breaks state persistence |
| Print `> ` prompt without newline | Standard interactive shell convention; flushes for immediate feedback | Other formats - less familiar to users |

## Codebase Analysis

### Existing Command Pattern

All commands follow this pattern (from `Command` base class):
```python
def execute(self, args: Namespace, service: TaskService) -> int:
    """Execute the command."""
    # Implementation
```

This signature is compatible with session mode -只需要 pass the shared service instance.

### Main Entry Point

Current `main.py` uses:
```python
def main():
    parser = ArgumentParser(...)
    # ... configure subparsers ...
    args = parser.parse_args()
    # ... execute single command ...
```

Interactive mode requires:
```python
if not sys.argv[1:]:  # No arguments = interactive mode
    interactive_session()
else:
    main()  # Existing behavior
```

### InMemoryTaskRepository

Already thread-safe for single-threaded use (no thread synchronization needed for synchronous CLI).
