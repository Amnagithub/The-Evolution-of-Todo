# Phase 3: AI-Powered Todo Web Application

A full-stack web application for multi-user task management with an AI chatbot assistant, evolving from Phase 2 to include natural language task management capabilities.

## Live Demo

**Live Application:** [https://ai-chatbot-the-evolution-of-todo-4j.vercel.app/dashboard](https://ai-chatbot-the-evolution-of-todo-4j.vercel.app/dashboard)

**Demo Video:** [Watch on Google Drive](https://drive.google.com/file/d/1mMOedA8kA3Cv353Dv9sdovnRFJ0HfEh5/view?usp=sharing)

## Overview

Phase 3 extends the web application with an AI-powered chatbot that enables natural language task management:
- User authentication (signup, signin, signout)
- Personal task management per user
- **AI Chatbot Assistant** - Manage tasks using natural language
- Real-time task updates
- Cloud-based PostgreSQL storage

## Tech Stack

### Frontend
- **Next.js 14** - React framework with App Router
- **Better Auth** - Authentication library with JWT support
- **Tailwind CSS** - Utility-first CSS framework
- **TypeScript** - Type-safe JavaScript

### Backend
- **FastAPI** - Modern Python web framework
- **SQLModel** - SQL database ORM with Pydantic integration
- **PyJWT** - JWT token verification
- **Uvicorn** - ASGI server

### Database
- **Neon Postgres** - Serverless PostgreSQL database

### Infrastructure
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration

## Project Structure

```
phase 2/
├── frontend/           # Next.js frontend application
│   ├── app/            # App Router pages
│   ├── components/     # React components
│   ├── lib/            # Auth and API utilities
│   └── Dockerfile
├── backend/            # FastAPI backend application
│   ├── models/         # SQLModel database models
│   ├── routes/         # API route handlers
│   ├── middleware/     # JWT authentication middleware
│   └── Dockerfile
├── phase-1/            # Original CLI application (reference)
├── specs/              # Feature specifications
├── history/            # Development history records
├── docker-compose.yml  # Docker orchestration
└── .env.example        # Environment variables template
```

## Features

- **User Authentication** - Secure signup and signin with JWT sessions
- **Task CRUD Operations** - Create, read, update, and delete tasks
- **Completion Toggle** - Mark tasks as complete/incomplete
- **User Isolation** - Each user only sees their own tasks
- **Optimistic Updates** - Instant UI feedback with rollback on error
- **AI Chatbot Assistant** - Natural language task management
  - "Add buy groceries" - Create new tasks
  - "Show my tasks" - List all tasks
  - "Done buy groceries" - Mark tasks complete
  - Floating chat widget with smooth animations

## API Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/health` | Health check | No |
| GET | `/api/tasks` | List user's tasks | Yes |
| POST | `/api/tasks` | Create a task | Yes |
| GET | `/api/tasks/{id}` | Get task by ID | Yes |
| PUT | `/api/tasks/{id}` | Update a task | Yes |
| DELETE | `/api/tasks/{id}` | Delete a task | Yes |
| PATCH | `/api/tasks/{id}/complete` | Toggle completion | Yes |

## Getting Started

### Prerequisites

- Node.js 18+
- Python 3.12+
- Docker (optional)
- Neon Postgres database account

### Environment Variables

Create a `.env` file in the phase 2 directory:

```env
DATABASE_URL=postgresql://user:password@host/database?sslmode=require
BETTER_AUTH_SECRET=your-secret-key
JWT_ALGORITHM=HS256
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Running Locally

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000 in your browser.

### Running with Docker

```bash
# Build and run all services
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build
```

Services:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Pages

| Route | Description | Auth Required |
|-------|-------------|---------------|
| `/` | Home - redirects based on auth status | No |
| `/signup` | User registration | No |
| `/signin` | User login | No |
| `/tasks` | Task management dashboard | Yes |

## Development

### Backend Development
```bash
cd backend
uvicorn main:app --reload  # Auto-reload on changes
```

### Frontend Development
```bash
cd frontend
npm run dev    # Development server with hot reload
npm run build  # Production build
npm run lint   # Run ESLint
```

## Architecture

The application follows a clean separation of concerns:

1. **Frontend** handles user interface and authentication state
2. **Backend** manages business logic and data persistence
3. **JWT tokens** provide stateless authentication between services
4. **Neon Postgres** provides scalable, serverless database storage

## License

MIT License - See LICENSE file for details.
