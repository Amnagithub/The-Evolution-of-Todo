# Quality Checklist: Task Organization Feature

**Feature ID:** 004-task-organization
**Spec Source:** `/mnt/c/Users/TLS/Documents/GitHub/The-Evolution-of-Todo/phase-1/specs/task-organization.md`
**Created:** 2026-01-02
**Version:** 1.0

---

## Checklist Summary

| Category | P0 | P1 | P2 | Total |
|----------|----|----|----|-------|
| Priority Management | 5 | 0 | 0 | 5 |
| Tag Management | 6 | 0 | 0 | 6 |
| Search Functionality | 5 | 0 | 0 | 5 |
| Filter Functionality | 5 | 0 | 0 | 5 |
| Sort Functionality | 6 | 0 | 0 | 6 |
| List Enhancement | 4 | 0 | 0 | 4 |
| Add/Update Enhancement | 4 | 0 | 0 | 4 |
| Data Persistence | 3 | 0 | 0 | 3 |
| Error Handling | 10 | 0 | 0 | 10 |
| Edge Cases | 8 | 2 | 0 | 10 |
| **Totals** | **56** | **2** | **0** | **58** |

---

## 1. Priority Management

### P0 - Must Have

| ID | Checklist Item | Pass Condition | Fail Condition |
|----|----------------|----------------|----------------|
| **PC-001** | Task creation accepts valid priority values | `todo add "test" --priority HIGH` creates task with priority HIGH | Task rejects HIGH priority or throws validation error |
| **PC-002** | Task creation accepts MEDIUM priority | `todo add "test" --priority MEDIUM` creates task with priority MEDIUM | Task rejects MEDIUM priority |
| **PC-003** | Task creation accepts LOW priority | `todo add "test" --priority LOW` creates task with priority LOW | Task rejects LOW priority |
| **PC-004** | Default priority is MEDIUM when not specified | `todo add "test"` creates task with priority MEDIUM (implicit) | Task created with null/None priority or different default |
| **PC-005** | Priority can be updated via update command | `todo update 1 --priority HIGH` changes task 1 priority to HIGH | Priority update fails or does not persist change |
| **PC-006** | Priority displayed in list output | `todo list` shows priority column with values HIGH/MEDIUM/LOW | Priority not visible in list output |
| **PC-007** | Priority displayed in search output | `todo search "test"` shows priority for each matching task | Priority not visible in search results |
| **PC-008** | Priority displayed in filter output | `todo filter --status ACTIVE` shows priority for each filtered task | Priority not visible in filter results |
| **PC-009** | Priority sorting orders HIGH > MEDIUM > LOW | `todo sort priority` lists HIGH tasks first, then MEDIUM, then LOW | Priority order incorrect in sort output |

---

## 2. Tag Management

### P0 - Must Have

| ID | Checklist Item | Pass Condition | Fail Condition |
|----|----------------|----------------|----------------|
| **TC-001** | Tasks can be created with zero tags | `todo add "test"` creates task with empty tags list `[]` | Task requires at least one tag |
| **TC-002** | Tasks can be created with multiple tags | `todo add "test" --tag work --tag urgent` creates task with 2 tags | Multiple tags not accepted on creation |
| **TC-003** | Tags stored in lowercase | `todo add "test" --tag Work` results in tag "work" in storage | Tag stored as "Work" or mixed case |
| **TC-004** | Tags trimmed of whitespace | `todo add "test" --tag " work "` results in tag "work" | Tag retains leading/trailing whitespace |
| **TC-005** | Duplicate tags rejected on same task | `todo add "test" --tag work --tag work` results in single "work" tag or error | Duplicate tag appears twice in task.tags |
| **TC-006** | Tags can be added via add command | `todo add "test" --tag planning` adds tag to new task | --tag option not accepted on add |
| **TC-007** | Tags can be added via update command | `todo update 1 --add-tag urgent` adds "urgent" to task 1 | --add-tag option not accepted or does not add tag |
| **TC-008** | Tags can be removed via update command | `todo update 1 --remove-tag bug` removes "bug" from task 1 | --remove-tag option not accepted or does not remove tag |
| **TC-009** | Tags displayed in list output | `todo list` shows tags column with comma-separated values | Tags not visible in list output |
| **TC-010** | Tags displayed in search output | `todo search "test"` shows tags for each matching task | Tags not visible in search results |
| **TC-011** | Tags displayed in filter output | `todo filter --status ACTIVE` shows tags for each filtered task | Tags not visible in filter results |

---

## 3. Search Functionality

### P0 - Must Have

| ID | Checklist Item | Pass Condition | Fail Condition |
|----|----------------|----------------|----------------|
| **SC-001** | Search finds keyword in title | `todo search "api"` returns tasks with "api" in title | Tasks with matching title not found |
| **SC-002** | Search finds keyword in description | `todo search "endpoint"` returns tasks with matching description | Tasks with matching description not found |
| **SC-003** | Search is case-insensitive | `todo search "API"` returns same results as `todo search "api"` | Case-sensitive search returns different results |
| **SC-004** | Search accepts --status filter | `todo search "bug" --status ACTIVE` returns only active tasks matching "bug" | --status option not accepted or ignored |
| **SC-005** | Search accepts --priority filter | `todo search "urgent" --priority HIGH` returns only high-priority tasks | --priority option not accepted or ignored |
| **SC-006** | Search accepts --tag filter | `todo search "fix" --tag backend` returns only tasks tagged "backend" | --tag option not accepted or ignored |
| **SC-007** | Search reports count of matches | Output shows "Found N task(s) matching..." | Match count not displayed |
| **SC-008** | Search reports "No matching tasks" when no results | `todo search "nonexistent"` outputs "No tasks found matching..." | Generic error or no message displayed |

---

## 4. Filter Functionality

### P0 - Must Have

| ID | Checklist Item | Pass Condition | Fail Condition |
|----|----------------|----------------|----------------|
| **FC-001** | Filter accepts --status ACTIVE | `todo filter --status ACTIVE` returns only active tasks | --status ACTIVE not accepted or returns wrong tasks |
| **FC-002** | Filter accepts --status COMPLETED | `todo filter --status COMPLETED` returns only completed tasks | --status COMPLETED not accepted or returns wrong tasks |
| **FC-003** | Filter accepts --priority HIGH | `todo filter --priority HIGH` returns only high-priority tasks | --priority HIGH not accepted or returns wrong tasks |
| **FC-004** | Filter accepts --priority MEDIUM | `todo filter --priority MEDIUM` returns only medium-priority tasks | --priority MEDIUM not accepted or returns wrong tasks |
| **FC-005** | Filter accepts --priority LOW | `todo filter --priority LOW` returns only low-priority tasks | --priority LOW not accepted or returns wrong tasks |
| **FC-006** | Filter accepts --tag option | `todo filter --tag work` returns only tasks with "work" tag | --tag not accepted or returns wrong tasks |
| **FC-007** | Multiple filters use AND logic | `todo filter --status ACTIVE --priority HIGH` returns tasks that are BOTH active AND high priority | Returns tasks matching ANY filter (OR logic) |
| **FC-008** | Filter reports filter criteria | Output shows "Filtered N task(s) by: status=ACTIVE, priority=HIGH" | Filter criteria not displayed |
| **FC-009** | Filter reports "No matching tasks" when no results | `todo filter --status ARCHIVED` (if not implemented) outputs "No tasks match..." | Generic error or no message displayed |

---

## 5. Sort Functionality

### P0 - Must Have

| ID | Checklist Item | Pass Condition | Fail Condition |
|----|----------------|----------------|----------------|
| **SO-001** | Sort accepts title field | `todo sort title` sorts tasks alphabetically A-Z | --title not accepted or sorts incorrectly |
| **SO-002** | Title sort ascending is A-Z | `todo sort title` lists tasks from A to Z | Title sort descending or random order |
| **SO-003** | Sort accepts priority field | `todo sort priority` orders tasks by priority | --priority not accepted or sorts incorrectly |
| **SO-004** | Priority sort order HIGH > MEDIUM > LOW | `todo sort priority` lists HIGH first, then MEDIUM, then LOW | Priority order incorrect |
| **SO-005** | Sort accepts id field | `todo sort id` orders tasks by creation order | --id not accepted or sorts incorrectly |
| **SO-006** | ID sort orders oldest first | `todo sort id` lists tasks with lowest ID first | ID sort orders newest first |
| **SO-007** | Sort accepts created field | `todo sort created` orders tasks by creation date | --created not accepted or sorts incorrectly |
| **SO-008** | Created sort orders oldest first | `todo sort created` lists earliest created task first | Created sort orders newest first |
| **SO-009** | --reverse flag reverses sort order | `todo sort title --reverse` lists Z to A | --reverse not accepted or has no effect |
| **SO-010** | Sort reports task count and criteria | Output shows "Sorted N task(s) by: priority (descending)" | Sort criteria not displayed |

---

## 6. List Command Enhancement

### P0 - Must Have

| ID | Checklist Item | Pass Condition | Fail Condition |
|----|----------------|----------------|----------------|
| **LC-001** | List displays ID column | `todo list` output includes ID column | ID not visible in list |
| **LC-002** | List displays Status column | `todo list` output includes Status column | Status not visible in list |
| **LC-003** | List displays Priority column | `todo list` output includes Priority column | Priority not visible in list |
| **LC-004** | List displays Title column | `todo list` output includes Title column | Title not visible in list |
| **LC-005** | List displays Tags column | `todo list` output includes Tags column | Tags not visible in list |
| **LC-006** | List --extended shows description | `todo list --extended` includes description field | Description not visible with --extended |
| **LC-007** | Tags formatted as comma-separated list in brackets | `todo list` shows `[bug, backend]` for tasks with multiple tags | Tags not formatted correctly |
| **LC-008** | Priority formatted as label | `todo list` shows `HIGH`, `MEDIUM`, `LOW` (not numeric/enum values) | Priority not in expected label format |

---

## 7. Add/Update Enhancement

### P0 - Must Have

| ID | Checklist Item | Pass Condition | Fail Condition |
|----|----------------|----------------|----------------|
| **AC-001** | Add command accepts --description | `todo add "test" --description "detailed desc"` creates task with description | --description not accepted |
| **AC-002** | Add command accepts --priority | `todo add "test" --priority HIGH` creates task with priority | --priority not accepted |
| **AC-003** | Add command accepts --tag | `todo add "test" --tag work` creates task with tag | --tag not accepted |
| **AC-004** | Update command accepts --description | `todo update 1 --description "new desc"` updates task description | --description not accepted |
| **AC-005** | Update command accepts --priority | `todo update 1 --priority LOW` updates task priority | --priority not accepted |
| **AC-006** | Update command accepts --add-tag | `todo update 1 --add-tag urgent` adds tag to task | --add-tag not accepted |
| **AC-007** | Update command accepts --remove-tag | `todo update 1 --remove-tag bug` removes tag from task | --remove-tag not accepted |
| **AC-008** | Update output shows changed values | `todo update 1 --priority HIGH` output shows `priority: HIGH (was MEDIUM)` | Old value not displayed in output |

---

## 8. Data Persistence

### P0 - Must Have

| ID | Checklist Item | Pass Condition | Fail Condition |
|----|----------------|----------------|----------------|
| **DP-001** | Priority persisted to storage | Task with priority HIGH saved to JSON storage, retrieved with same priority | Priority resets to default after restart |
| **DP-002** | Tags persisted to storage | Task with tags ["work", "urgent"] saved to JSON storage, retrieved with same tags | Tags lost after restart |
| **DP-003** | Task IDs increment correctly | Add tasks, restart, add more tasks - IDs are sequential without gaps | ID collisions or gaps after restart |
| **DP-004** | Description persisted to storage | Task with description saved and retrieved with same description | Description lost after restart |

---

## 9. Error Handling

### P0 - Must Have

| ID | Error Scenario | Expected Message | Pass Condition | Fail Condition |
|----|----------------|------------------|----------------|----------------|
| **EH-001** | Invalid priority value | "Invalid priority. Must be HIGH, MEDIUM, or LOW." | `todo add "test" --priority INVALID` shows correct error | Wrong error message or exception |
| **EH-002** | Invalid status value | "Invalid status. Must be ACTIVE or COMPLETED." | `todo filter --status INVALID` shows correct error | Wrong error message or exception |
| **EH-003** | Empty title on add | "Task title cannot be empty." | `todo add ""` shows correct error | Wrong error message or exception |
| **EH-004** | Empty title on update | "Task title cannot be empty." | `todo update 1 --title ""` shows correct error | Wrong error message or exception |
| **EH-005** | Title too long (>200 chars) | "Task title must be 200 characters or less." | `todo add "x"*201` shows correct error | Wrong error message or exception |
| **EH-006** | Duplicate tag on add | "Tag '{tag}' already exists on this task." | `todo update 1 --add-tag existing` shows correct error | Wrong error message or exception |
| **EH-007** | Tag to remove not found | "Tag '{tag}' not found on this task." | `todo update 1 --remove-tag nonexistent` shows correct error | Wrong error message or exception |
| **EH-008** | Task ID not found | "Task with ID {id} not found." | `todo complete 9999` shows correct error | Wrong error message or exception |
| **EH-009** | No tasks match filter | "No tasks match the specified filter." | `todo filter --status ACTIVE` (when no active tasks) shows correct error | Wrong error message or exception |
| **EH-010** | No tasks match search | "No tasks found matching '{keyword}'." | `todo search "xyz"` (no results) shows correct error | Wrong error message or exception |
| **EH-011** | Invalid sort field | "Invalid sort field. Must be: title, priority, id, created." | `todo sort invalid` shows correct error | Wrong error message or exception |

---

## 10. Edge Cases and Boundary Conditions

### P0 - Must Have

| ID | Edge Case | Expected Behavior | Pass Condition | Fail Condition |
|----|-----------|-------------------|----------------|----------------|
| **EC-001** | Search with empty keyword | Error or no results | `todo search ""` shows error or returns no tasks | Crashes or returns all tasks |
| **EC-002** | Filter with no criteria | Shows all tasks (same as list) | `todo filter` outputs all tasks | Error or empty result |
| **EC-003** | Sort with single task | Task displayed correctly | `todo sort title` with 1 task shows that task | Error or missing task |
| **EC-004** | Task with maximum title length (200 chars) | Accepted and stored | `todo add "x"*200` succeeds | Rejected or truncated |
| **EC-005** | Task with title length 201 chars | Rejected with error | `todo add "x"*201` shows title length error | Accepted or wrong error |
| **EC-006** | Remove last tag from task | Task has empty tags list | `todo update 1 --remove-tag onlytag` results in `[]` | Error or null tags |
| **EC-007** | Add tag that differs only by case | Normalized to lowercase | `todo update 1 --add-tag WORK` when "work" exists shows duplicate error | Two tags "work" and "WORK" exist |
| **EC-008** | Search with special regex characters | Treated as literal text | `todo search "[test]"` finds tasks with literal brackets | Regex error or wrong results |
| **EC-009** | Update priority same as current | No change, output shows same value | `todo update 1 --priority HIGH` (already HIGH) shows no change | Error or inconsistent output |
| **EC-010** | Multiple tags with different cases added | All normalized to lowercase | `todo add "test" --tag A --tag B` results in ["a", "b"] | Case preserved or mixed case |

### P1 - Should Have

| ID | Edge Case | Expected Behavior | Pass Condition | Fail Condition |
|----|-----------|-------------------|----------------|----------------|
| **EC-011** | Empty tag string | Ignored or error | `todo add "test" --tag ""` either ignores or shows error | Crashes or creates empty string tag |
| **EC-012** | Whitespace-only tag | Trimmed to empty or error | `todo add "test" --tag "   "` either trims or shows error | Creates tag with spaces |

---

## 11. Invariants (Always True)

The following conditions must always hold true during and after any operation:

| ID | Invariant | Verification Method |
|----|-----------|---------------------|
| **INV-001** | Task ID is unique across all tasks | No two tasks share the same ID |
| **INV-002** | Task ID is always a positive integer | IDs are 1, 2, 3, ... never 0 or negative |
| **INV-003** | Title is never empty after any operation | All tasks have non-empty title strings |
| **INV-004** | Title never exceeds 200 characters | All tasks have title length <= 200 |
| **INV-005** | Priority is always set (never None) | Every task has priority HIGH, MEDIUM, or LOW |
| **INV-006** | Tags list contains only unique, lowercase, trimmed strings | No duplicates, all lowercase, no leading/trailing whitespace |
| **INV-007** | created_at is set on creation and never modified | created_at equals initial value after any update |
| **INV-008** | updated_at is always >= created_at | Timestamp invariant maintained |
| **INV-009** | Status is always a valid TaskStatus enum value | No string or invalid status values stored |
| **INV-010** | Tags are unique per task (no duplicates) | tags list has all unique elements |

---

## 12. CLI Command Matrix

| Command | New/Modified | Required Options | Required Arguments |
|---------|--------------|------------------|-------------------|
| `add` | Modified | `--priority`, `--tag` (optional), `--description` (optional) | `<title>` |
| `update` | Modified | `--priority`, `--add-tag`, `--remove-tag`, `--description` (optional) | `<id>` |
| `list` | Modified | `--extended` (optional) | None |
| `search` | New | `--status`, `--priority`, `--tag` (all optional) | `<keyword>` |
| `filter` | New | `--status`, `--priority`, `--tag` (all optional) | None |
| `sort` | New | `--reverse` (optional) | `<field>` |
| `complete` | Preserved | None | `<id>` |
| `incomplete` | Preserved | None | `<id>` |
| `delete` | Preserved | None | `<id>` |
| `help` | Preserved | None | None |

---

## 13. Verification Commands

Run these commands to verify implementation:

```bash
# Priority tests
todo add "High priority task" --priority HIGH
todo add "Medium priority task"
todo add "Low priority task" --priority LOW
todo list | grep -E "HIGH|MEDIUM|LOW"
todo update 1 --priority LOW

# Tag tests
todo add "Tagged task" --tag work --tag urgent
todo list | grep -E "\[.*\]"
todo update 1 --add-tag backend
todo update 1 --remove-tag urgent

# Search tests
todo search "task"
todo search "task" --status ACTIVE
todo search "task" --priority HIGH
todo search "task" --tag work

# Filter tests
todo filter --status ACTIVE
todo filter --priority HIGH
todo filter --tag work
todo filter --status ACTIVE --priority HIGH

# Sort tests
todo sort title
todo sort priority
todo sort id
todo sort created
todo sort title --reverse

# List tests
todo list
todo list --extended

# Error tests
todo add ""  # Should fail: empty title
todo add "test" --priority INVALID  # Should fail: invalid priority
todo complete 9999  # Should fail: task not found
```

---

## 14. Sign-Off Checklist

Before marking this feature as complete, verify:

- [ ] All P0 items pass
- [ ] All P1 items pass
- [ ] All invariants hold true
- [ ] Error messages match specification exactly
- [ ] Output formats match specification examples
- [ ] Data persists correctly across restarts
- [ ] No data loss or corruption
- [ ] No crashes on invalid input
- [ ] Case-insensitive operations verified
- [ ] Tag normalization verified

---

*Generated from specification: `/mnt/c/Users/TLS/Documents/GitHub/The-Evolution-of-Todo/phase-1/specs/task-organization.md`*
