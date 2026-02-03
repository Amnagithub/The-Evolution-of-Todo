# Research: Phase II - Full-Stack Todo Web Application

**Feature**: 006-fullstack-todo
**Date**: 2026-01-15
**Status**: Complete

## Overview

This document consolidates research findings for the Phase II full-stack implementation. All technical decisions have been resolved based on project requirements and industry best practices.

---

## Research Topics

### 1. JWT Authentication Flow (Frontend ↔ Backend)

**Decision**: Better Auth (frontend) generates JWT → PyJWT (backend) verifies

**Rationale**:
- Better Auth provides built-in JWT plugin with refresh token handling
- PyJWT is the standard Python library for JWT decoding/verification
- Shared secret (BETTER_AUTH_SECRET) enables independent verification
- No session database sharing required between frontend and backend

**Alternatives Considered**:
- **Shared session DB**: Rejected - adds coupling between services, single point of failure
- **OAuth2 provider**: Rejected - overkill for single-app auth, adds external dependency
- **Custom JWT implementation**: Rejected - reinvents wheel, security risks

**Implementation Pattern**:
```
Frontend (Next.js + Better Auth):
  1. User signs up/in → Better Auth creates session
  2. Better Auth JWT plugin generates access token
  3. Token stored in localStorage/cookie
  4. API client attaches token to Authorization header

Backend (FastAPI + PyJWT):
  1. Middleware intercepts request
  2. Extract token from "Authorization: Bearer <token>"
  3. Verify signature using BETTER_AUTH_SECRET
  4. Extract user_id from payload
  5. Attach user_id to request state
  6. Route handlers filter by request.state.user_id
```

---

### 2. Better Auth Configuration

**Decision**: Use Better Auth with JWT plugin for Next.js 14+ App Router

**Rationale**:
- Native TypeScript support
- Built-in JWT plugin simplifies token management
- Supports App Router with server components
- Active maintenance and documentation

**Configuration Requirements**:
- Database adapter: Neon Postgres (for user storage)
- JWT plugin enabled with shared secret
- Session strategy: JWT (not database sessions)
- Cookie settings: httpOnly, secure in production

**Key Files**:
- `/lib/auth.ts` - Better Auth server configuration
- `/lib/auth-client.ts` - Client-side auth hooks
- `/app/api/auth/[...all]/route.ts` - Auth API routes

---

### 3. SQLModel Best Practices

**Decision**: SQLModel for ORM with Pydantic v2 integration

**Rationale**:
- Created by FastAPI author (tiangolo)
- Native Pydantic model integration
- Cleaner than SQLAlchemy for simple CRUD
- Automatic request/response validation

**Alternatives Considered**:
- **SQLAlchemy Core**: Rejected - more verbose, no Pydantic integration
- **Tortoise ORM**: Rejected - async-only, less FastAPI ecosystem support
- **Raw SQL**: Rejected - no type safety, maintenance burden

**Best Practices Applied**:
```python
# Model definition with table=True
class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    completed: bool = False
    user_id: str = Field(index=True, foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Separate request/response schemas (no table=True)
class TaskCreate(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None

class TaskUpdate(SQLModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
```

---

### 4. Neon Postgres Connection

**Decision**: Connection pooling via Neon serverless driver

**Rationale**:
- Neon provides serverless Postgres with connection pooling
- Handles cold starts efficiently
- Compatible with SQLModel/SQLAlchemy
- Free tier sufficient for development

**Connection Pattern**:
```python
from sqlmodel import create_engine, Session

DATABASE_URL = os.getenv("DATABASE_URL")  # Neon connection string
engine = create_engine(DATABASE_URL, echo=False)

def get_session():
    with Session(engine) as session:
        yield session
```

**Environment Variables**:
- `DATABASE_URL`: Neon Postgres connection string (pooled)
- `BETTER_AUTH_SECRET`: Shared JWT signing secret

---

### 5. Docker Compose Configuration

**Decision**: Multi-container setup with environment variable sharing

**Rationale**:
- Frontend and backend as separate containers
- Shared .env file for secrets
- Network isolation with internal communication
- Easy local development and testing

**Service Configuration**:
```yaml
services:
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - BETTER_AUTH_SECRET=${BETTER_AUTH_SECRET}
      - NEXT_PUBLIC_API_URL=http://backend:8000
    depends_on:
      - backend

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - BETTER_AUTH_SECRET=${BETTER_AUTH_SECRET}
```

---

### 6. API Client Pattern (Frontend)

**Decision**: Centralized API client with automatic auth header injection

**Rationale**:
- Single source of truth for API calls
- Automatic token attachment
- Error handling centralized
- Type-safe with TypeScript

**Implementation Pattern**:
```typescript
// /lib/api.ts
export const api = {
  async get<T>(path: string): Promise<T> {
    const token = await getToken();
    const res = await fetch(`${API_URL}${path}`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    if (!res.ok) throw new ApiError(res.status);
    return res.json();
  },
  // post, put, patch, delete methods...
};
```

---

### 7. User Isolation Security

**Decision**: All queries filtered by user_id from JWT at middleware level

**Rationale**:
- Defense in depth: middleware extracts user_id, routes use it
- No user_id in URL prevents enumeration attacks
- 404 returned for other users' resources (not 403)
- Prevents accidental data leakage

**Security Pattern**:
```python
# Middleware extracts user_id
@app.middleware("http")
async def verify_jwt(request: Request, call_next):
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        request.state.user_id = payload["sub"]
    except jwt.InvalidTokenError:
        return JSONResponse(status_code=401, content={"error": "Invalid token"})
    return await call_next(request)

# Routes always filter by user_id
@router.get("/tasks")
def list_tasks(request: Request, session: Session = Depends(get_session)):
    user_id = request.state.user_id
    return session.exec(select(Task).where(Task.user_id == user_id)).all()
```

---

## Resolved Clarifications

| Original Unknown | Resolution | Source |
|-----------------|------------|--------|
| JWT token format | Better Auth default (HS256, sub=user_id) | Better Auth docs |
| Token storage | localStorage with httpOnly cookie fallback | Security best practices |
| DB migration strategy | SQLModel create_all() for MVP | SQLModel docs |
| Password hashing | Better Auth built-in (bcrypt) | Better Auth internals |
| CORS configuration | Allow frontend origin only | FastAPI middleware |

---

## Technology Stack Summary

| Layer | Technology | Version | Purpose |
|-------|------------|---------|---------|
| Frontend Framework | Next.js | 14+ | React SSR/SSG with App Router |
| Frontend Auth | Better Auth | Latest | JWT authentication |
| Frontend Styling | Tailwind CSS | 3.x | Utility-first CSS |
| Backend Framework | FastAPI | 0.100+ | Python async API |
| Backend ORM | SQLModel | 0.0.14+ | Pydantic + SQLAlchemy |
| Backend JWT | PyJWT | 2.x | JWT verification |
| Database | Neon Postgres | Latest | Serverless Postgres |
| Container | Docker Compose | 3.8+ | Multi-container orchestration |

---

## Next Phase

Research complete. Proceed to Phase 1:
1. `data-model.md` - Entity definitions
2. `contracts/openapi.yaml` - API specification
3. `quickstart.md` - Developer setup guide
