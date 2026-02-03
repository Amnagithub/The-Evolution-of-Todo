# CLI Contract: list Command (Extended)

**Command**: `list`
**Type**: Modified Command
**Spec Reference**: task-organization.md §4.2.2

## Synopsis

```
todo list [--extended]
```

## Options

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--extended` | flag | False | Show full details including description, priority, and tags |

## Outputs

### Compact Output (Default)

```
ID  Status    Priority  Title                      Tags
1   ACTIVE    HIGH      [bug] API endpoint returns 500  [bug, backend]
2   ACTIVE    MEDIUM    API documentation                 [docs]
3   COMPLETED LOW       Initial setup                      []
```

### Extended Output (`--extended`)

```
ID  Status    Priority  Title                      Tags
1   ACTIVE    HIGH      [bug] API endpoint returns 500  [bug, backend]
2   ACTIVE    MEDIUM    API documentation                 [docs]
3   COMPLETED LOW       Initial setup                      []

Showing 3 task(s).

Task Details:
[1] Write API spec
    Description: Create OpenAPI specification for the REST API
    Priority: HIGH | Tags: [planning, backend]
    Created: 2026-01-02 08:00 | Updated: 2026-01-02 08:00
    Status: ACTIVE

[2] Fix login bug
    Description: OAuth flow fails on mobile
    Priority: HIGH | Tags: [bug, auth]
    Created: 2026-01-02 09:00 | Updated: 2026-01-02 10:30
    Status: ACTIVE
```

### Empty List

```
No tasks found. Use 'todo add <title>' to create a task.

Showing 0 task(s).
```

## Format Specifications

| Column | Width | Alignment | Content |
|--------|-------|-----------|---------|
| ID | 3 | Right | Task ID |
| Status | 8 | Left | ACTIVE / COMPLETED |
| Priority | 8 | Left | HIGH / MEDIUM / LOW |
| Title | 25+ | Left | Task title (truncated if >25) |
| Tags | 15+ | Left | Comma-separated tags in brackets |

## Changes from Previous Version

- Added Priority column
- Added Tags column
- Status shows ACTIVE instead of PENDING
- Added `--extended` flag for full details
- Extended output shows all task fields including description
