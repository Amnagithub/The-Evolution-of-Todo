"""FastAPI application entry point."""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from database import init_db
from routes import tasks_router, chat_router


class DebugCORSMiddleware(BaseHTTPMiddleware):
    """Temporary debug middleware to log CORS requests."""
    async def dispatch(self, request: Request, call_next):
        origin = request.headers.get("origin", "NO_ORIGIN")
        method = request.method
        path = request.url.path
        if method == "OPTIONS":
            print(f"[DEBUG CORS] {method} {path} - Origin: {origin}")
        return await call_next(request)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup."""
    init_db()
    yield


app = FastAPI(
    title="Phase II Todo API",
    description="RESTful API for multi-user task management with session authentication.",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        # Local development
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
        "http://frontend:3000",
        # Vercel production deployments
        "https://the-evolution-of-todo.vercel.app",
        "https://*.vercel.app",
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept", "X-Requested-With"],
)

# Debug middleware (added last = runs first, before CORS)
app.add_middleware(DebugCORSMiddleware)

# Register routes
app.include_router(tasks_router)
app.include_router(chat_router)


@app.get("/")
def root():
    """Root endpoint."""
    return {"message": "Phase II Todo API", "docs": "/docs"}


@app.get("/health")
def health_check():
    """Health check endpoint (no auth required)."""
    from datetime import datetime
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat()
    }
