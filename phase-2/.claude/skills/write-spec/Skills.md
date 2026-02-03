name: write-spec
description: Writes structured Spec-Kit specs (features/API/DB/UI). Use when planning new features or updates in Phase II.

## Write Spec-Kit Specification

### Instructions

1. Read project reqs, @specs/overview.md, .spec-kit/config.yaml.
2. Determine category: features/, api/, database/, ui/.
3. Structure spec: Title, User Stories, Acceptance Criteria (detailed, testable), Examples, Edge Cases.
4. Phase II focus: Task CRUD (title/desc/completed, user-owned), JWT auth (Bearer header, backend verify).
5. Write to /specs/[category]/filename.md. Reference DB schema (tasks.user_id FK).
6. Output: Full markdown spec + Write file.

```
spec-kit write /specs/....
```

### Examples

**Feature Spec:**
```markdown
# Task CRUD

## User Stories
- As user, create task w/ title.

## AC
- POST /api/tasks: title req (1-200 chars), auto user_id.
```

**API Spec:**
```markdown
# REST Endpoints

### POST /api/tasks
Req: {title: str, desc?: str}
Auth: Bearer JWT → extract user_id.
```
