# Research: Task Organization Feature

**Feature**: 004-task-organization
**Date**: 2026-01-02

## Research Questions

### RQ-001: Python dataclass default_factory patterns for mutable defaults

**Question**: How to properly initialize `tags: list[str]` as empty list default in dataclass?

**Decision**: Use `field(default_factory=list)` pattern

**Rationale**:
- Python dataclasses don't allow mutable defaults directly (they share state across instances)
- `field(default_factory=list)` creates a new empty list for each instance
- This is the official Python pattern documented in dataclasses documentation

**Implementation**:
```python
from dataclasses import dataclass, field

@dataclass
class Task:
    tags: list[str] = field(default_factory=list)
```

**Alternatives Considered**:
- `tags: list[str] = []` - WRONG: shares list across all instances
- `tags: list[str] | None = None` - OK but requires None check on every access

---

### RQ-002: Python enum auto() vs explicit values

**Question**: Should Priority enum use `auto()` or explicit string values?

**Decision**: Use explicit string values matching spec

**Rationale**:
- String values serialize/deserialize naturally to JSON
- Human-readable in storage file (`.todo/tasks.json`)
- Explicit values make debugging easier

**Implementation**:
```python
class Priority(Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
```

**Alternatives Considered**:
- `auto()` - Returns integers (1, 2, 3), less readable in storage
- String-based with custom names - Over-engineering for simple enum

---

### RQ-003: argparse append action for multiple --tag values

**Question**: How to handle multiple `--tag` flags in argparse?

**Decision**: Use `action='append'` with type normalization

**Rationale**:
- `action='append'` collects each `--tag` into a list
- Each tag can be normalized (lowercase, trimmed) during parsing
- Matches common CLI patterns (e.g., `pip install -r requirements.txt`)

**Implementation**:
```python
parser.add_argument('--tag', action='append', dest='tags',
                    help='Tag to add (can be specified multiple times)')
```

**Output**: `args.tags` will be `['planning', 'backend']` for `--tag planning --tag backend`

**Alternatives Considered**:
- Comma-separated: `--tag planning,backend` - Harder for users, requires parsing
- JSON array: `--tag '["planning", "backend"]'` - Too complex for CLI

---

### RQ-004: In-memory filtering vs repository query methods

**Question**: Should filter/search operations use repository query methods or in-memory filtering?

**Decision**: Use in-memory filtering with existing repository get_all()

**Rationale**:
- Phase I storage is JSON file with in-memory list
- Dataset size expected < 1000 tasks (no performance concern)
- Existing `get_all_tasks()` already returns sorted list
- Simpler code path, less repository interface changes

**Implementation**:
```python
def filter_tasks(self, status=None, priority=None, tag=None):
    tasks = self._repo.get_all()
    if status:
        tasks = [t for t in tasks if t.status == status]
    if priority:
        tasks = [t for t in tasks if t.priority == priority]
    if tag:
        tasks = [t for t in tasks if tag.lower() in [t.lower() for t in t.tags]]
    return sorted(tasks, key=lambda t: t.id)
```

**Alternatives Considered**:
- Repository query methods - Would require storage index optimization, premature for Phase I
- Database-style queries - Over-engineering for file-based storage

---

### RQ-005: Tag normalization strategy

**Question**: When and where should tags be normalized (lowercase, trimmed)?

**Decision**: Normalize at input boundary (CLI argument parsing)

**Rationale**:
- Single place for normalization logic
- Consistent behavior across all tag operations
- Easier to test and maintain

**Implementation**:
```python
def _normalize_tag(tag: str) -> str:
    return tag.strip().lower()

# In argparse type or after parsing:
normalized_tags = [_normalize_tag(t) for t in input_tags]
```

**Valid tag patterns**:
- `"planning"` → `"planning"`
- `"  PLANNING  "` → `"planning"`
- `"Planning"` → `"planning"`

**Invalid patterns** (to reject):
- Empty strings after trimming
- Tags with special characters (allow letters, numbers, hyphens, underscores)

---

### RQ-006: Priority sorting order

**Question**: How to implement HIGH > MEDIUM > LOW sorting?

**Decision**: Use enum member value order with reverse sort flag

**Rationale**:
- Python enums maintain declaration order (since Python 3.10)
- Explicit values (HIGH="HIGH") sort alphabetically, which happens to match priority order
- Simple reverse flag for LOW > MEDIUM > HIGH

**Implementation**:
```python
priority_order = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}
sorted_tasks = sorted(tasks, key=lambda t: priority_order[t.priority])
```

**Alternatives Considered**:
- Custom `__lt__` on Priority - More complex, affects all comparisons
- Integer values (0, 1, 2) - Less readable in storage

---

### RQ-007: TaskStatus naming (PENDING vs ACTIVE)

**Question**: Spec shows ACTIVE but existing code uses PENDING. Which to use?

**Decision**: Keep PENDING internally, add ACTIVE as alias for CLI output

**Rationale**:
- Existing code already uses TaskStatus.PENDING
- Changing would require modifying all existing tests and commands
- CLI can display "ACTIVE" while domain uses "PENDING"
- Backward compatible with existing storage format

**Implementation**:
```python
class TaskStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"

    @property
    def display_name(self) -> str:
        return "ACTIVE" if self == PENDING else self.name
```

**Alternatives Considered**:
- Rename to ACTIVE - Breaking change for existing code
- Add ACTIVE as duplicate - Confusing redundancy

---

## Consolidated Decisions

| ID | Decision | Key Rationale |
|----|----------|---------------|
| RQ-001 | `field(default_factory=list)` | Official Python pattern, no shared state |
| RQ-002 | Explicit string enum values | Human-readable, natural JSON serialization |
| RQ-003 | `action='append'` | Standard argparse pattern for multiple values |
| RQ-004 | In-memory filtering | Dataset size doesn't warrant complex queries |
| RQ-005 | Normalize at CLI boundary | Single source of truth, easier testing |
| RQ-006 | Priority order dict | Explicit control over sort order |
| RQ-007 | PENDING internally, ACTIVE in display | Backward compatible, no breaking changes |

## References

- [Python dataclasses - Default factory](https://docs.python.org/3/library/dataclasses.html#default-factory-functions)
- [Python enum - Values](https://docs.python.org/3/library/enum.html#enum.Enum)
- [argparse - append action](https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_argument)
