name: implement-crud
description: Implements CRUD endpoints + UI from spec. Use for feature-implementer on task-crud/authentication. Covers backend/frontend.

## Implement CRUD Full-Stack

### Instructions

1. Read spec @specs/features/task-crud.md, @specs/api/rest-endpoints.md, CLAUDE.md files.
2. Backend (/backend/): Add SQLModel Task model (user_id: str FK), routes/tasks.py (GET/POST/PUT/DELETE/PATCH /api/tasks, filter by auth user_id), JWT middleware (decode via PyJWT, shared BETTER_AUTH_SECRET).
3. Frontend (/frontend/): Better Auth setup (JWT plugin), /app/tasks/page.tsx (list/create/update), /lib/api.ts (fetch w/ auth token), Tailwind UI table/form.
4. Integration: docker-compose.yml (backend:8000, neon proxy).
5. Generate Claude Code prompts: "Impl backend @specs/...".
6. Test: `curl -H "Authorization: Bearer <token>" /api/tasks`.

### Examples

**Backend Prompt:**
```
Per backend/CLAUDE.md, add to main.py:

@app.middleware("http")
async def verify_jwt(request):
    decode token → user_id or raise 401.
```

**Frontend:**
```typescript
import { api } from '@/lib/api'

const tasks = await api.get('/tasks', {
  headers: { Authorization: `Bearer ${token}` }
})
```
