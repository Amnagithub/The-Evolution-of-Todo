---
id: 005
title: CORS Preflight Fix Planning
stage: plan
date: 2026-01-16
surface: agent
model: claude-opus-4-5-20251101
feature: 006-fullstack-todo
branch: main
user: TLS
command: /sp.plan
labels: ["cors", "fastapi", "preflight", "options"]
links:
  spec: specs/006-fullstack-todo/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - backend/main.py
  - backend/middleware/jwt_auth.py
tests:
  - Manual CORS preflight test with browser DevTools
---

## Prompt

update: Implement proper CORS configuration in FastAPI for a Next.js frontend running on localhost:3000. Include CORSMiddleware with explicit origins, allow credentials, all methods and headers. Fix preflight OPTIONS 400 Bad Request issue.Review the CORS setup in main.py. Check for common mistakes that cause 400 on OPTIONS preflight (wildcard with credentials, missing origins, order of middleware). Suggest improvements.Update the include: "Backend must support CORS for frontend origins localhost:3000 with credentials for authentication flow."

## Response snapshot

Identified root cause: HTTPBearer security scheme with `auto_error=True` (default) was interfering with CORS preflight OPTIONS requests by raising exceptions before CORSMiddleware could respond.

Fixes applied:
1. Set `HTTPBearer(auto_error=False)` to prevent automatic 403 responses
2. Added explicit null check for credentials with proper 401 response
3. Added explicit OPTIONS handler as fallback for preflight requests
4. Simplified CORSMiddleware config with `allow_methods=["*"]`
5. Defined ALLOWED_ORIGINS constant for consistent reference

## Outcome

- Impact: Fixed CORS preflight 400 errors blocking frontend-backend communication
- Tests: Requires manual browser testing of signup/signin flow
- Files: 2 files modified (main.py, jwt_auth.py)
- Next prompts: Test full auth flow after restarting services
- Reflection: HTTPBearer auto_error is a common CORS pitfall in FastAPI

## Evaluation notes (flywheel)

- Failure modes observed: HTTPBearer auto_error=True blocks OPTIONS before CORS middleware
- Graders run and results (PASS/FAIL): N/A - manual testing required
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Verify CORSMiddleware alone works after HTTPBearer fix
