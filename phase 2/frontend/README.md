# Todo Frontend

Next.js 14 frontend for the Phase II Todo Web Application with Better Auth authentication.

## Tech Stack

- **Next.js 14** - React framework with App Router
- **Better Auth** - Authentication library with JWT support
- **Tailwind CSS** - Utility-first CSS framework
- **TypeScript** - Type-safe JavaScript

## Prerequisites

- Node.js 18+
- Backend API running on port 8000
- Environment variables configured

## Environment Variables

Create a `.env` file in the project root (parent directory):

```env
BETTER_AUTH_SECRET=your-secret-key
NEXT_PUBLIC_API_URL=http://localhost:8000
DATABASE_URL=postgresql://user:password@host/database?sslmode=require
```

## Installation

```bash
# Install dependencies
npm install

# Run development server
npm run dev
```

Open http://localhost:3000 in your browser.

## Pages

| Route | Description | Auth Required |
|-------|-------------|---------------|
| `/` | Home - redirects based on auth status | No |
| `/signup` | User registration | No |
| `/signin` | User login | No |
| `/tasks` | Task management dashboard | Yes |

## Features

- **User Authentication** - Sign up, sign in, sign out with JWT sessions
- **Task CRUD** - Create, read, update, delete tasks
- **Completion Toggle** - Mark tasks as complete/incomplete
- **Optimistic Updates** - Instant UI feedback with rollback on error
- **User Isolation** - Each user only sees their own tasks

## Project Structure

```
frontend/
├── app/
│   ├── layout.tsx       # Root layout
│   ├── page.tsx         # Home page (redirect logic)
│   ├── globals.css      # Global styles
│   ├── signin/
│   │   └── page.tsx     # Sign in page
│   ├── signup/
│   │   └── page.tsx     # Sign up page
│   ├── tasks/
│   │   └── page.tsx     # Task dashboard
│   └── api/
│       └── auth/
│           └── [...all]/
│               └── route.ts  # Better Auth API routes
├── components/
│   ├── AuthGuard.tsx    # Route protection
│   ├── Header.tsx       # Navigation header
│   ├── TaskForm.tsx     # Task creation form
│   └── TaskList.tsx     # Task list with edit/delete
├── lib/
│   ├── auth.ts          # Better Auth server config
│   ├── auth-client.ts   # Client-side auth hooks
│   └── api.ts           # API client with JWT
├── package.json
├── tsconfig.json
├── tailwind.config.ts
├── postcss.config.js
├── next.config.js
└── Dockerfile
```

## Components

### AuthGuard
Protects routes - redirects to `/signin` if not authenticated.

### TaskForm
Form for creating new tasks with title (required) and description (optional).

### TaskList
Displays tasks with:
- Completion checkbox
- Inline editing
- Delete with confirmation
- Created date display

## API Client

The `lib/api.ts` client automatically:
- Attaches JWT token to requests
- Points to `NEXT_PUBLIC_API_URL`
- Handles JSON serialization

## Running with Docker

```bash
docker build -t todo-frontend .
docker run -p 3000:3000 --env-file ../.env todo-frontend
```

## Scripts

```bash
npm run dev      # Development server
npm run build    # Production build
npm run start    # Production server
npm run lint     # ESLint check
```
