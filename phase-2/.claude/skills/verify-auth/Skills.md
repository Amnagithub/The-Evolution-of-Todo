name: verify-auth
description: Verifies auth/JWT integration, security, user isolation. Use for qa-reviewer post-impl. Runs checks/tests.

## Verify Authentication & Security

### Instructions

1. Grep monorepo: JWT in backend middleware, Better Auth config frontend.
2. Test flow: Signup → JWT token → API calls (expect user-specific tasks, 401 w/o token).
3. Check: Shared secret env, token expiry, no DB session share, filters (`tasks.query.where(Task.user_id == user_id)`).
4. Security: Input validation, indexes (user_id), no secrets hardcoded.
5. DB: Neon schema (`psql: SELECT * FROM tasks WHERE user_id='{id}'`).
6. Output: Pass/Fail report, fixes (e.g., "Add @app.exception_handler(401)").

### Examples

**Test Commands:**
```bash
# Backend
uvicorn main:app; curl -H "Auth: Bearer invalid" localhost:8000/api/tasks → 401

# Frontend
npm run dev; login → check localStorage token → tasks page loads own tasks only.
```

**Fix Example:**
```
Critical: No user filter → Add .filter(Task.user_id == jwt_user_id) to all queries.
```
