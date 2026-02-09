# Quickstart Guide: Phase II - Full-Stack Todo Web Application

**Feature**: 006-fullstack-todo
**Date**: 2026-01-15

## Prerequisites

- Docker and Docker Compose installed
- Node.js 18+ (for local frontend development)
- Python 3.11+ (for local backend development)
- Neon Postgres account (free tier available)

## Quick Start (Docker)

### 1. Clone and Setup Environment

```bash
# Navigate to project root
cd "phase 2"

# Copy environment template
cp .env.example .env
```

### 2. Configure Environment Variables

Edit `.env` with your values:

```env
# Database (Neon Postgres)
DATABASE_URL=postgresql://user:password@host.neon.tech/dbname?sslmode=require

# Authentication (shared secret between frontend and backend)
BETTER_AUTH_SECRET=your-secure-random-string-at-least-32-chars

# API URL (for frontend to call backend)
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Generate a secure secret**:
```bash
openssl rand -base64 32
```

### 3. Start Services

```bash
# Build and start all services
docker-compose up --build

# Or run in background
docker-compose up -d --build
```

### 4. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs (Swagger UI)

### 5. Verify Setup

```bash
# Check services are running
docker-compose ps

# View logs
docker-compose logs -f

# Health check
curl http://localhost:8000/health
```

---

## Local Development (Without Docker)

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL="your-neon-url"
export BETTER_AUTH_SECRET="your-secret"

# Run development server
uvicorn main:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Set environment variables
export BETTER_AUTH_SECRET="your-secret"
export NEXT_PUBLIC_API_URL="http://localhost:8000"

# Run development server
npm run dev
```

---

## Testing the API

### Get JWT Token (via Better Auth)

1. Navigate to http://localhost:3000/signup
2. Create an account
3. Open browser DevTools → Application → Local Storage
4. Copy the JWT token

### Test API Endpoints

```bash
# Set your token
TOKEN="your-jwt-token-here"

# List tasks (should return empty array initially)
curl -H "Authorization: Bearer $TOKEN" \
     http://localhost:8000/api/tasks

# Create a task
curl -X POST \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"title":"My first task","description":"Testing the API"}' \
     http://localhost:8000/api/tasks

# Get a specific task
curl -H "Authorization: Bearer $TOKEN" \
     http://localhost:8000/api/tasks/1

# Update a task
curl -X PUT \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"title":"Updated task title"}' \
     http://localhost:8000/api/tasks/1

# Toggle completion
curl -X PATCH \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"completed":true}' \
     http://localhost:8000/api/tasks/1/complete

# Delete a task
curl -X DELETE \
     -H "Authorization: Bearer $TOKEN" \
     http://localhost:8000/api/tasks/1
```

### Expected Responses

| Endpoint | Success | Auth Error |
|----------|---------|------------|
| GET /api/tasks | 200 + array | 401 |
| POST /api/tasks | 201 + task | 401 |
| GET /api/tasks/{id} | 200 + task | 401, 404 |
| PUT /api/tasks/{id} | 200 + task | 401, 404 |
| DELETE /api/tasks/{id} | 204 (no content) | 401, 404 |
| PATCH /api/tasks/{id}/complete | 200 + task | 401, 404 |

---

## Database Verification

### Connect to Neon Postgres

```bash
# Using psql
psql $DATABASE_URL

# Or use Neon Console web interface
```

### Verify User Isolation

```sql
-- Check tasks table exists
\dt tasks

-- View all tasks (admin view)
SELECT id, title, user_id, completed FROM tasks;

-- Verify user isolation
SELECT * FROM tasks WHERE user_id = 'specific-user-id';
```

---

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| 401 Unauthorized | Check BETTER_AUTH_SECRET matches in both services |
| Database connection failed | Verify DATABASE_URL includes `?sslmode=require` |
| CORS errors | Ensure frontend URL is in backend CORS origins |
| Port already in use | Stop conflicting services or change ports |

### Docker Logs

```bash
# View all logs
docker-compose logs

# View specific service
docker-compose logs frontend
docker-compose logs backend

# Follow logs in real-time
docker-compose logs -f
```

### Reset Everything

```bash
# Stop and remove containers
docker-compose down

# Remove volumes (deletes data)
docker-compose down -v

# Rebuild from scratch
docker-compose build --no-cache
docker-compose up
```

---

## Project Structure Reference

```text
phase 2/
├── docker-compose.yml
├── .env.example
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── models/
│   ├── routes/
│   └── middleware/
├── frontend/
│   ├── package.json
│   ├── app/
│   ├── lib/
│   └── components/
└── specs/006-fullstack-todo/
    ├── spec.md
    ├── plan.md
    ├── research.md
    ├── data-model.md
    ├── quickstart.md (this file)
    └── contracts/openapi.yaml
```

---

## Next Steps

1. Run `/sp.tasks` to generate implementation tasks
2. Use `feature-implementer` agent to execute implementation
3. Run `qa-reviewer` agent to validate security and isolation
