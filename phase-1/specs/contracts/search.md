# CLI Contract: search Command

**Command**: `search`
**Type**: New Command
**Spec Reference**: task-organization.md §4.1.1

## Synopsis

```
todo search <keyword> [--status <status>] [--priority <priority>] [--tag <tag>]
```

## Description

Search for tasks containing the specified keyword in title or description.

## Arguments

| Position | Name | Type | Required | Description |
|----------|------|------|----------|-------------|
| 1 | `keyword` | string | Yes | Text to search for (case-insensitive) |

## Options

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--status` | ACTIVE\|COMPLETED | None | Filter by task status |
| `--priority` | HIGH\|MEDIUM\|LOW | None | Filter by priority level |
| `--tag` | string | None | Filter by specific tag (case-insensitive) |

## Outputs

### Success - Results Found

```
Found {N} task(s) matching "{keyword}":

[{id}] {priority} [{tags}] {title}
     id: {id} | status: {status} | priority: {priority} | tags: [{tags}]
     created: {created_at} | updated: {updated_at}
```

### Success - No Results

```
No tasks found matching "{keyword}".
```

### Success - With Filters Applied

```
Found {N} task(s) matching "{keyword}" (status={status}, priority={priority}):

...
```

## Errors

| Error Code | Condition | Exit Code | Message |
|------------|-----------|-----------|---------|
| ERR-103 | No matching tasks | 0 | "No tasks found matching '{keyword}'." |
| ERR-001 | Invalid priority value | 1 | "Invalid priority. Must be HIGH, MEDIUM, or LOW." |
| ERR-002 | Invalid status value | 1 | "Invalid status. Must be ACTIVE or COMPLETED." |

## Examples

```bash
todo search "api"
todo search "bug" --status ACTIVE
todo search "urgent" --priority HIGH
todo search "project" --tag work
todo search "spec" --status ACTIVE --priority HIGH
```

## Implementation Notes

- Keyword search is case-insensitive
- Search matches in `title` OR `description` (if description exists)
- Multiple filters use AND logic
- Tags displayed as comma-separated list in brackets: `[tag1, tag2]`
- Empty tags list shown as `[]`
- Priority sorting: HIGH > MEDIUM > LOW (original order preserved within same priority)
