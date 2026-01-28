---
title: Todo Backend API
emoji: ⚡
colorFrom: purple
colorTo: pink
sdk: docker
sdk_version: "0.28.1"
python_version: "3.12"
app_file: main.py
pinned: false
---

# Todo Backend API

FastAPI backend for the Phase II Todo Web Application with JWT authentication and Neon Postgres database.

## Tech Stack

- **FastAPI** - Modern Python web framework
- **SQLModel** - SQL database ORM with Pydantic integration
- **PyJWT** - JWT token verification
- **Neon Postgres** - Serverless PostgreSQL database
- **Uvicorn** - ASGI server

## Prerequisites

- Python 3.12+
- Neon Postgres database
- Environment variables configured

## Environment Variables

Create a `.env` file in the project root (parent directory):

```env
DATABASE_URL=postgresql://user:password@host/database?sslmode=require
BETTER_AUTH_SECRET=your-secret-key
JWT_ALGORITHM=HS256
```

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/health` | Health check | No |
| GET | `/api/tasks` | List user's tasks | Yes |
| POST | `/api/tasks` | Create a task | Yes |
| GET | `/api/tasks/{id}` | Get task by ID | Yes |
| PUT | `/api/tasks/{id}` | Update a task | Yes |
| DELETE | `/api/tasks/{id}` | Delete a task | Yes |
| PATCH | `/api/tasks/{id}/complete` | Toggle completion | Yes |

## Authentication

All `/api/tasks` endpoints require a valid JWT token in the Authorization header:

```
Authorization: Bearer <token>
```

The JWT is issued by Better Auth on the frontend and verified using the shared `BETTER_AUTH_SECRET`.

## Project Structure

```
backend/
├── main.py              # FastAPI app entry point
├── database.py          # Database connection
├── requirements.txt     # Python dependencies
├── Dockerfile           # Container configuration
├── models/
│   ├── __init__.py
│   └── task.py          # Task SQLModel
├── routes/
│   ├── __init__.py
│   └── tasks.py         # Task CRUD endpoints
└── middleware/
    ├── __init__.py
    └── jwt_auth.py      # JWT verification
```

## Task Model

```python
{
  "id": 1,
  "title": "Task title",
  "description": "Optional description",
  "completed": false,
  "user_id": "user-uuid",
  "created_at": "2026-01-15T00:00:00",
  "updated_at": "2026-01-15T00:00:00"
}
```

## Running with Docker

```bash
docker build -t todo-backend .
docker run -p 8000:8000 --env-file ../.env todo-backend
```
