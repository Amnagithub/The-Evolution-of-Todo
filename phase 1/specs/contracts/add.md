# CLI Contract: add Command (Extended)

**Command**: `add`
**Type**: Modified Command
**Spec Reference**: task-organization.md §4.2.1

## Synopsis

```
todo add <title> [--description <desc>] [--priority <priority>] [--tag <tag>...]
```

## Arguments

| Position | Name | Type | Required | Description |
|----------|------|------|----------|-------------|
| 1 | `title` | string | Yes | Task title (1-200 characters) |

## Options

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--description` | string | None | Detailed task description (optional) |
| `--priority` | HIGH\|MEDIUM\|LOW | MEDIUM | Priority level |
| `--tag` | string (repeatable) | None | Tag to add (can be specified multiple times) |

## Outputs

### Success

```
Task added: [{id}] {title}
     priority: {priority} | tags: [{tags}]
```

### Validation Errors

| Error Code | Condition | Exit Code | Message |
|------------|-----------|-----------|---------|
| ERR-003 | Empty title | 1 | "Task title cannot be empty." |
| ERR-004 | Title > 200 chars | 1 | "Task title must be 200 characters or less." |
| ERR-001 | Invalid priority | 1 | "Invalid priority. Must be HIGH, MEDIUM, or LOW." |

## Examples

```bash
todo add "Write API spec"
todo add "Fix login bug" --priority HIGH --tag bug
todo add "Update docs" --priority LOW --tag docs --description "Update README"
todo add "Refactor" --tag refactor --tag backend
```

## Changes from Previous Version

- Added `--description` option
- Added `--priority` option (default: MEDIUM)
- Added `--tag` option (repeatable)
- Output now includes priority and tags
