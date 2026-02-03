# CLI Contract: update Command (Extended)

**Command**: `update`
**Type**: Modified Command
**Spec Reference**: task-organization.md §4.2.3

## Synopsis

```
todo update <id> [--title <title>] [--description <desc>] [--priority <priority>] [--add-tag <tag>] [--remove-tag <tag>]
```

## Arguments

| Position | Name | Type | Required | Description |
|----------|------|------|----------|-------------|
| 1 | `id` | int | Yes | Task ID to update |

## Options

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--title` | string | None | Update task title |
| `--description` | string | None | Update task description (use empty string to clear) |
| `--priority` | HIGH\|MEDIUM\|LOW | None | Update priority level |
| `--add-tag` | string (repeatable) | None | Add a tag (can be specified multiple times) |
| `--remove-tag` | string (repeatable) | None | Remove a tag (can be specified multiple times) |

## Outputs

### Success - Single Change

```
Task updated: [{id}] {title}
     priority: {priority} (was {old_priority})
```

### Success - Multiple Changes

```
Task updated: [{id}] {title}
     priority: {priority} (was {old_priority}) | tags: [{new_tags}] (removed: [{removed_tags}])
```

### Success - Title Change

```
Task updated: [{id}] {old_title} → {new_title}
```

### Success - Tag Changes

```
Task updated: [{id}] {title}
     tags: [{new_tags}] (added: [{added_tags}]) (removed: [{removed_tags}])
```

## Errors

| Error Code | Condition | Exit Code | Message |
|------------|-----------|-----------|---------|
| ERR-101 | Task ID not found | 1 | "Task with ID {id} not found." |
| ERR-003 | Empty title | 1 | "Task title cannot be empty." |
| ERR-004 | Title > 200 chars | 1 | "Task title must be 200 characters or less." |
| ERR-001 | Invalid priority | 1 | "Invalid priority. Must be HIGH, MEDIUM, or LOW." |
| ERR-005 | Duplicate tag on add | 1 | "Tag '{tag}' already exists on this task." |
| ERR-006 | Tag to remove not found | 1 | "Tag '{tag}' not found on this task." |

## Examples

```bash
todo update 1 --priority HIGH
todo update 1 --add-tag urgent --remove-tag bug
todo update 1 --description "Detailed description here"
todo update 1 --title "New title" --priority LOW
todo update 1 --add-tag planning --add-tag backend
todo update 1 --remove-tag urgent
```

## Changes from Previous Version

- Added `--description` option
- Added `--priority` option
- Added `--add-tag` option (repeatable)
- Added `--remove-tag` option (repeatable)
- Output shows changed values with old → new format
