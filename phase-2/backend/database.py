"""Database connection and session management for Neon Postgres or SQLite."""
import os
from pathlib import Path
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy import text
from dotenv import load_dotenv

# Load .env from the backend directory explicitly
backend_dir = Path(__file__).resolve().parent
load_dotenv(backend_dir / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")

# Debug: log which database is being used
print(f"[DEBUG DB] DATABASE_URL set: {bool(DATABASE_URL)}")

# Use SQLite for local development if DATABASE_URL is not set
if not DATABASE_URL:
    # Use absolute path so frontend and backend share the same database
    sqlite_path = backend_dir / "todo.db"
    print(f"DATABASE_URL not set - using SQLite at: {sqlite_path}")
    DATABASE_URL = f"sqlite:///{sqlite_path}"
    IS_SQLITE = True
else:
    IS_SQLITE = DATABASE_URL.startswith("sqlite")

# Create engine with connection pooling (SQLite doesn't support pool_pre_ping)
engine_kwargs = {"echo": False}
if not IS_SQLITE:
    engine_kwargs["pool_pre_ping"] = True
else:
    # SQLite needs check_same_thread=False for FastAPI
    engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, **engine_kwargs)


def run_migrations():
    """Run database migrations to add missing columns."""
    with engine.connect() as conn:
        if IS_SQLITE:
            # SQLite: Check if priority column exists using PRAGMA
            result = conn.execute(text("PRAGMA table_info(tasks)"))
            columns = [row[1] for row in result.fetchall()]
            if "priority" not in columns:
                print("Adding 'priority' column to tasks table...")
                conn.execute(text(
                    "ALTER TABLE tasks ADD COLUMN priority VARCHAR(20) DEFAULT 'medium'"
                ))
                conn.commit()
                print("Migration completed: 'priority' column added.")
        else:
            # PostgreSQL: Check if priority column exists
            result = conn.execute(text("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = 'tasks' AND column_name = 'priority'
            """))
            if result.fetchone() is None:
                print("Adding 'priority' column to tasks table...")
                conn.execute(text("""
                    ALTER TABLE tasks
                    ADD COLUMN priority VARCHAR(20) NOT NULL DEFAULT 'medium'
                """))
                conn.commit()
                print("Migration completed: 'priority' column added.")


def init_db():
    """Initialize database tables and run migrations."""
    SQLModel.metadata.create_all(engine)
    run_migrations()


def get_session():
    """Dependency for FastAPI routes to get a database session."""
    with Session(engine) as session:
        yield session
