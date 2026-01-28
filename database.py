"""Database connection and session management for Neon Postgres."""
import os
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy import text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# Create engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
)


def run_migrations():
    """Run database migrations to add missing columns."""
    with engine.connect() as conn:
        # Check if priority column exists
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
