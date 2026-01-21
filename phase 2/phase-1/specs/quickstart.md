# Quickstart: Task Organization Feature

**Feature**: 004-task-organization
**Date**: 2026-01-02

## Overview

This guide helps developers set up, understand, and test the Task Organization feature for the Todo CLI.

## Prerequisites

- Python 3.11 or higher
- uv (package manager) or pip
- Git

## Setup

### 1. Clone and Install

```bash
# Navigate to the project root
cd /mnt/c/Users/TLS/Documents/GitHub/The-Evolution-of-Todo

# Install dependencies with uv
uv pip install -e ".[dev]"

# Or with pip
pip install -e ".[dev]"

# Install pytest
pip install pytest
```

### 2. Verify Installation

```bash
# Check todo command is available
todo --help

# Expected output:
# usage: todo <command> [<args>]
# commands:
#   add         Add a new task
#   list        List all tasks
#   ...
```

### 3. Run Existing Tests

```bash
# Run all tests
pytest tests/ -v

# Expected: All Phase 1 tests pass (59 tests)
```

## Project Structure

```
phase-1/source/todo/
├── domain/
│   ├── entities.py      # Task entity (modify: add priority, tags, updated_at)
│   ├── value_objects.py # Priority enum, TaskStatus (add display_name)
│   ├── repository.py    # TaskRepository (add query methods)
│   └── errors.py        # Add ValidationError subclasses
├── services/
│   └── task_service.py  # TaskService (add search, filter, sort methods)
└── cli/
    ├── main.py          # Add search, filter, sort subparsers
    └── commands/
        ├── add.py       # Add --priority, --tag, --description
        ├── list.py      # Add --extended, update output
        ├── update.py    # Add --priority, --add-tag, --remove-tag
        ├── search.py    # NEW
        ├── filter.py    # NEW
        └── sort.py      # NEW
```

## Key Changes Summary

### Domain Layer

1. **value_objects.py** - Add `Priority` enum, update `TaskStatus` with `display_name`
2. **entities.py** - Add `priority`, `tags`, `updated_at` fields; add methods for tag management
3. **repository.py** - Add optional query methods (can be service-layer only)

### Service Layer

1. **task_service.py** - Add:
   - `create_task()` with priority and tags parameters
   - `update_task()` with priority and tag management
   - `search_tasks()` for keyword search
   - `filter_tasks()` for criteria-based filtering
   - `sort_tasks()` for sorting by field

### CLI Layer

1. **main.py** - Add subparsers for `search`, `filter`, `sort` commands
2. **add.py** - Add `--priority`, `--tag`, `--description` arguments
3. **list.py** - Add `--extended` flag, update output format
4. **update.py** - Add `--priority`, `--add-tag`, `--remove-tag`, `--description`
5. **search.py** - New file implementing search command
6. **filter.py** - New file implementing filter command
7. **sort.py** - New file implementing sort command

## Development Workflow

### 1. Run Tests Before Changes

```bash
pytest tests/ -v --tb=short
```

### 2. Implement Domain Changes First

```bash
# Implement value_objects.py with Priority enum
# Run unit tests for value_objects
pytest tests/unit/domain/ -v

# Implement entities.py with new fields
# Run unit tests for entities
pytest tests/unit/domain/test_task.py -v
```

### 3. Implement Service Changes

```bash
# Implement task_service.py methods
# Run integration tests
pytest tests/integration/ -v
```

### 4. Implement CLI Commands

```bash
# Implement each command
# Run CLI tests
pytest tests/cli/ -v
```

### 5. End-to-End Testing

```bash
# Clear existing data
rm -f .todo/tasks.json

# Test complete workflow
todo add "Task 1" --priority HIGH --tag work
todo add "Task 2" --priority MEDIUM --tag personal
todo list --extended
todo search "Task"
todo filter --priority HIGH
todo sort priority
todo update 1 --add-tag urgent
todo list
```

## Testing Commands

### Priority Tests

```bash
# Test priority creation
todo add "High priority task" --priority HIGH
todo add "Low priority task" --priority LOW

# Test priority sorting
todo sort priority
# Expected: High priority first
```

### Tag Tests

```bash
# Test tag creation
todo add "Tagged task" --tag work --tag urgent

# Test tag filtering
todo filter --tag urgent

# Test tag update
todo update 1 --add-tag new-tag --remove-tag urgent
```

### Search Tests

```bash
# Test search
todo add "Searchable task with unique keyword XYZ123"
todo search XYZ123
# Expected: Found task with XYZ123

todo search "nonexistent"
# Expected: No tasks found
```

### Filter Tests

```bash
# Test combined filters
todo filter --status ACTIVE --priority HIGH
todo filter --tag work
```

### Sort Tests

```bash
# Test different sort fields
todo sort title
todo sort priority
todo sort id
todo sort created
todo sort title --reverse
```

## Common Issues

### Issue: Tags Not Persisting

**Cause**: Forgetting to call repository save after tag modification.

**Fix**: Ensure `self._repo.save(task)` is called after any tag changes.

### Issue: Priority Sorting Wrong Order

**Cause**: Using alphabetical sort on enum names instead of defined order.

**Fix**: Use explicit priority order dict: `{Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}`

### Issue: Duplicate Tags Allowed

**Cause**: Not checking for existing tags before adding.

**Fix**: Add validation in `add_tag()` method to check for duplicates (case-insensitive).

### Issue: Empty Tags Shown Incorrectly

**Cause**: Not handling empty list in output formatting.

**Fix**: Use `[]` for empty tags list in all output formats.

## Validation Checklist

Before committing, verify:

- [ ] All existing tests pass (`pytest tests/ -v`)
- [ ] New unit tests added for domain changes
- [ ] New integration tests added for service changes
- [ ] New CLI tests added for search, filter, sort commands
- [ ] Tag normalization works (lowercase, trimmed)
- [ ] Priority default is MEDIUM
- [ ] Error messages match spec contracts
- [ ] Output format matches spec examples
- [ ] Backward compatibility with existing commands maintained

## Next Steps

1. Run `/sp.tasks` to generate ordered implementation task list
2. Execute tasks in order with Claude Code
3. Run tests after each task completion
4. Update this quickstart with any gotchas discovered
