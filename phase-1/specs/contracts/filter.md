# CLI Contract: filter Command

**Command**: `filter`
**Type**: New Command
**Spec Reference**: task-organization.md §4.1.2

## Synopsis

```
todo filter [--status <status>] [--priority <priority>] [--tag <tag>]
```

## Description

Filter tasks based on specified criteria. Multiple filters are ANDed together.

## Arguments

None (all parameters are optional flags).

## Options

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--status` | ACTIVE\|COMPLETED | None | Show only tasks with specific status |
| `--priority` | HIGH\|MEDIUM\|LOW | None | Show only tasks with specific priority |
| `--tag` | string | None | Show only tasks with specific tag (case-insensitive) |

## Outputs

### Success - Results Found

```
Filtered {N} task(s) by: {criteria}

[{id}] {priority} [{tags}] {title}
     id: {id} | status: {status} | priority: {priority} | tags: [{tags}]
     created: {created_at} | updated: {updated_at}
```

### Success - No Arguments (All Tasks)

```
{output from list command}

Showing {N} task(s).
```

### Success - No Results

```
No tasks match the specified filter.
```

### Success - With Multiple Filters

```
Filtered {N} task(s) by: status={status}, priority={priority}, tag={tag}

...
```

## Errors

| Error Code | Condition | Exit Code | Message |
|------------|-----------|-----------|---------|
| ERR-102 | No matching tasks | 0 | "No tasks match the specified filter." |
| ERR-001 | Invalid priority value | 1 | "Invalid priority. Must be HIGH, MEDIUM, or LOW." |
| ERR-002 | Invalid status value | 1 | "Invalid status. Must be ACTIVE or COMPLETED." |

## Examples

```bash
todo filter
todo filter --status ACTIVE
todo filter --priority HIGH
todo filter --tag work
todo filter --status ACTIVE --priority HIGH
todo filter --priority MEDIUM --tag backend
```

## Implementation Notes

- No arguments shows all tasks (same as `list`)
- Multiple filters use AND logic (all must match)
- Display criteria list in sorted order: status, priority, tag
- If no filters match any task, exit code 0 with informational message
