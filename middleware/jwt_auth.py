"""Session-based authentication middleware for FastAPI.

Verifies Better Auth session tokens by querying the database directly.
"""
import os
from datetime import datetime, timezone
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, select, text
from dotenv import load_dotenv

from database import get_session as get_db_session

load_dotenv()

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
    if credentials is None:
        raise AuthError("Authorization header missing")

    session_token = credentials.credentials

    try:
        # Query Better Auth's session table directly
        # Better Auth creates a "session" table with token and userId columns
        result = db.execute(
            text("""
                SELECT "userId", "expiresAt"
                FROM "session"
                WHERE "token" = :token
            """),
            {"token": session_token}
        )
        row = result.fetchone()

        if not row:
            raise AuthError("Invalid session token")

        user_id, expires_at = row

        # Check if session is expired
        if expires_at:
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
        print(f"[DEBUG AUTH] Database error: {e}")
        raise AuthError(f"Authentication error: {str(e)}")
