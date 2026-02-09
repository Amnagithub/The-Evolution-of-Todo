"""Session-based authentication middleware for FastAPI.

Verifies Better Auth session tokens by querying the database directly.
Supports DEV_MODE for local development without database setup.
"""
import os
from pathlib import Path
from datetime import datetime, timezone
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, select, text
from dotenv import load_dotenv

from database import get_session as get_db_session

# Load .env from the backend directory explicitly
backend_dir = Path(__file__).resolve().parent.parent
load_dotenv(backend_dir / ".env")

# Development mode: bypass authentication when DATABASE_URL is not set
# This allows local development without needing a shared PostgreSQL database
DEV_MODE = os.getenv("DEV_MODE", "").lower() in ("true", "1", "yes")
DEV_USER_ID = os.getenv("DEV_USER_ID", "dev-user-local")

if DEV_MODE:
    print("[AUTH] DEV_MODE enabled - authentication bypassed, using dev user")

security = HTTPBearer(auto_error=False)


class AuthError(HTTPException):
    """Custom exception for authentication errors."""
    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(status_code=401, detail=detail)


async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
    db: Session = Depends(get_db_session)
) -> str:
    """
    Verify session token by querying Better Auth's session table directly.

    Args:
        credentials: Bearer token (session token) from Authorization header
        db: Database session

    Returns:
        user_id extracted from the session

    Raises:
        AuthError: If session is invalid or expired
    """
    # Development mode bypass - return dev user without checking credentials
    if DEV_MODE:
        return DEV_USER_ID

    if credentials is None:
        raise AuthError("Authorization header missing")

    session_token = credentials.credentials

    # Better Auth signs tokens in format: {token}.{signature}
    # Extract just the token part for database lookup
    if session_token and '.' in session_token:
        session_token = session_token.split('.')[0]

    # Debug: log the received token with length
    print(f"[DEBUG AUTH] Token for lookup (len={len(session_token) if session_token else 0}): {session_token}")

    try:
        # Debug: show which database we're connected to
        from database import DATABASE_URL, IS_SQLITE
        print(f"[DEBUG AUTH] Using SQLite: {IS_SQLITE}, DB: {DATABASE_URL[:50] if DATABASE_URL else 'None'}...")

        # Query Better Auth's session table directly
        # Better Auth uses different column names for SQLite vs PostgreSQL
        if IS_SQLITE:
            # SQLite: Better Auth uses snake_case
            query = text("""
                SELECT userId, expiresAt
                FROM session
                WHERE token = :token
            """)
        else:
            # PostgreSQL: Better Auth uses camelCase with quotes
            query = text("""
                SELECT "userId", "expiresAt"
                FROM "session"
                WHERE "token" = :token
            """)

        result = db.execute(query, {"token": session_token})
        row = result.fetchone()

        # Debug: log if row was found
        print(f"[DEBUG AUTH] Session row found: {row is not None}")

        # If not found, show what tokens exist (first 20 chars)
        if row is None:
            if IS_SQLITE:
                result2 = db.execute(text('SELECT token FROM session LIMIT 5'))
            else:
                result2 = db.execute(text('SELECT token FROM "session" LIMIT 5'))
            existing = [r[0][:20] + '...' for r in result2.fetchall()]
            print(f"[DEBUG AUTH] Sample existing tokens: {existing}")

        if not row:
            raise AuthError("Invalid session token")

        user_id, expires_at = row

        # Check if session is expired
        if expires_at:
            # Parse string dates (SQLite stores as ISO strings)
            if isinstance(expires_at, str):
                # Handle ISO format with Z suffix
                expires_at = expires_at.replace('Z', '+00:00')
                expires_at = datetime.fromisoformat(expires_at)

            # Handle both naive and aware datetimes
            now = datetime.utcnow()
            if hasattr(expires_at, 'tzinfo') and expires_at.tzinfo is not None:
                now = datetime.now(timezone.utc)
            if expires_at < now:
                raise AuthError("Session expired")

        if not user_id:
            raise AuthError("Session missing user identifier")

        return user_id

    except AuthError:
        raise
    except Exception as e:
        error_msg = str(e)
        print(f"[DEBUG AUTH] Database error: {e}")
        if "no such table" in error_msg.lower() or "session" in error_msg.lower():
            raise AuthError("Session table not found. Ensure Better Auth has initialized the database.")
        raise AuthError(f"Authentication error: {error_msg}")
