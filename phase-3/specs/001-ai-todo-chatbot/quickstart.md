# Quickstart: AI Todo Chatbot (Phase III)

**Branch**: `001-ai-todo-chatbot`
**Date**: 2026-02-05

---

## Prerequisites

- Phase II application running (backend + frontend)
- Neon PostgreSQL database configured
- Better Auth working with sessions
- Python 3.11+ and Node.js 18+
- OpenAI API key

---

## Environment Variables

Add to your `.env` file:

```bash
# Existing Phase II variables
DATABASE_URL=postgresql://user:pass@host/db
BETTER_AUTH_SECRET=your-secret-at-least-32-chars

# New Phase III variables
OPENAI_API_KEY=sk-your-openai-api-key
OPENAI_MODEL=gpt-4-turbo-preview  # or gpt-4o
```

---

## Quick Setup

### 1. Install Backend Dependencies

```bash
cd backend
pip install openai mcp
# or add to requirements.txt:
# openai>=1.6.0
# mcp>=0.9.0
```

### 2. Install Frontend Dependencies

```bash
cd frontend
npm install framer-motion
```

### 3. Run Database Migration

```bash
cd backend
alembic upgrade head
# This adds: conversation, message tables
```

### 4. Start the Application

```bash
# Terminal 1: Backend
cd backend
uvicorn main:app --reload

# Terminal 2: Frontend
cd frontend
npm run dev
```

### 5. Access the Chat

Open `http://localhost:3000` and look for the chat widget in the bottom-right corner.

---

## Testing the Chat

Try these commands:

```
User: add buy groceries
Bot:  Added buy groceries (ID 1) ✓

User: show my tasks
Bot:  Here are your tasks:
      • buy groceries (pending)

User: done buy groceries
Bot:  Marked buy groceries as done ✓

User: who am I?
Bot:  You are john_doe (created 2025-01-15)
```

---

## Project Structure (after Phase III)

```
phase-3/
├── backend/
│   ├── main.py              # Add chat router
│   ├── models/
│   │   ├── task.py          # Existing
│   │   ├── conversation.py  # NEW
│   │   └── message.py       # NEW
│   ├── routes/
│   │   ├── tasks.py         # Existing
│   │   └── chat.py          # NEW
│   ├── tools/               # NEW: MCP tools
│   │   ├── __init__.py
│   │   ├── add_task.py
│   │   ├── list_tasks.py
│   │   ├── complete_task.py
│   │   ├── delete_task.py
│   │   ├── update_task.py
│   │   └── get_user_details.py
│   └── agent/               # NEW: OpenAI Agent
│       ├── __init__.py
│       └── todo_agent.py
├── frontend/
│   ├── components/
│   │   ├── ChatWidget.tsx   # NEW: Floating chat
│   │   ├── ChatMessage.tsx  # NEW: Message bubble
│   │   ├── TypingIndicator.tsx  # NEW
│   │   └── ...existing
│   └── app/
│       └── layout.tsx       # Modified: Add ChatWidget
└── specs/
    └── 001-ai-todo-chatbot/
        ├── spec.md
        ├── plan.md
        ├── research.md
        ├── data-model.md
        ├── quickstart.md    # This file
        └── contracts/
            ├── chat-api.yaml
            └── mcp-tools.json
```

---

## API Endpoints

### Send Message
```bash
POST /api/chat
Authorization: Bearer {session_token}
Content-Type: application/json

{"message": "add buy groceries"}
```

### Get History
```bash
GET /api/chat/history?limit=50
Authorization: Bearer {session_token}
```

### Clear History
```bash
DELETE /api/chat/clear
Authorization: Bearer {session_token}
```

---

## Troubleshooting

### Chat widget not appearing
- Check browser console for errors
- Verify user is authenticated
- Check z-index conflicts with other UI elements

### "Unauthorized" errors
- Session may have expired - sign in again
- Verify `Authorization` header is being sent

### Agent not calling tools correctly
- Check OpenAI API key is valid
- Review agent logs in backend console
- Verify tool schemas match expected format

### Animations janky on mobile
- Enable `prefers-reduced-motion` in device settings
- Check for heavy CSS/JS on page

---

## Next Steps

1. Run `/sp.tasks` to generate detailed implementation tasks
2. Start with database models and migrations
3. Implement MCP tools
4. Build the chat endpoint and agent
5. Add the frontend chat widget
6. Write tests
