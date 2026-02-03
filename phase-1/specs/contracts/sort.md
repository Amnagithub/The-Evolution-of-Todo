# CLI Contract: sort Command

**Command**: `sort`
**Type**: New Command
**Spec Reference**: task-organization.md §4.1.3

## Synopsis

```
todo sort <field> [--reverse]
```

## Description

Display tasks sorted by the specified field.

## Arguments

| Position | Name | Type | Required | Description |
|----------|------|------|----------|-------------|
| 1 | `field` | string | Yes | Field to sort by: `title`, `priority`, `id`, `created` |

## Options

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--reverse` | flag | False | Sort in descending order instead of ascending |

## Outputs

### Success - Results Found

```
Sorted {N} task(s) by: {field} ({order})

[{id}] {priority} [{tags}] {title}
     id: {id} | status: {status} | priority: {priority} | tags: [{tags}]
     created: {created_at} | updated: {updated_at}
```

### Success - Empty List

```
No tasks to sort.
```

### Success - Reverse Sort

```
Sorted {N} task(s) by: {field} (descending)

...
```

## Errors

| Error Code | Condition | Exit Code | Message |
|------------|-----------|-----------|---------|
| ERR-104 | Invalid sort field | 1 | "Invalid sort field. Must be: title, priority, id, created." |

## Sort Field Behavior

| Field | Ascending | Descending | Notes |
|-------|-----------|------------|-------|
| `title` | A-Z | Z-A | Case-insensitive alphabetical |
| `priority` | HIGH > MEDIUM > LOW | LOW > MEDIUM > HIGH | Priority enum order |
| `id` | Oldest first (1, 2, 3) | Newest first (3, 2, 1) | Creation order |
| `created` | Oldest first | Newest first | By created_at timestamp |

## Examples

```bash
todo sort title
todo sort priority
todo sort id
todo sort created
todo sort title --reverse
todo sort priority --reverse
todo sort id --reverse
```

## Implementation Notes

- Default sort order is ascending (A-Z, HIGH to LOW)
- `--reverse` flag reverses the sort order
- Title sort is case-insensitive ("app" comes before "Zebra")
- Priority sort uses sort order: HIGH=0, MEDIUM=1, LOW=2
- ID sort matches creation order (lower ID = created earlier)
