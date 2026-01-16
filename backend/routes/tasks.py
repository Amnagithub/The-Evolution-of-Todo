"""Task CRUD endpoints with JWT authentication."""
from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from database import get_session
from models import Task, TaskCreate, TaskUpdate, TaskToggle, TaskResponse
from middleware import get_current_user_id

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


def task_to_response(task: Task) -> TaskResponse:
    """Convert Task model to response (excludes user_id)."""
    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        created_at=task.created_at,
        updated_at=task.updated_at,
    )


@router.get("", response_model=List[TaskResponse])
def list_tasks(
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    """List all tasks for the authenticated user, sorted by newest first."""
    statement = (
        select(Task)
        .where(Task.user_id == user_id)
        .order_by(Task.created_at.desc())
    )
    tasks = session.exec(statement).all()
    return [task_to_response(task) for task in tasks]


@router.post("", response_model=TaskResponse, status_code=201)
def create_task(
    task_data: TaskCreate,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    """Create a new task for the authenticated user."""
    # Validate title has non-whitespace content
    if not task_data.title.strip():
        raise HTTPException(status_code=422, detail="Title must contain non-whitespace characters")

    task = Task(
        title=task_data.title.strip(),
        description=task_data.description,
        user_id=user_id,
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task_to_response(task)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    """Get a specific task by ID (only if owned by authenticated user)."""
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task_to_response(task)


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    """Update a task (only if owned by authenticated user)."""
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Update fields if provided
    if task_data.title is not None:
        if not task_data.title.strip():
            raise HTTPException(status_code=422, detail="Title must contain non-whitespace characters")
        task.title = task_data.title.strip()

    if task_data.description is not None:
        task.description = task_data.description

    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)
    return task_to_response(task)


@router.patch("/{task_id}/complete", response_model=TaskResponse)
def toggle_task_complete(
    task_id: int,
    toggle_data: TaskToggle,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    """Toggle task completion status (only if owned by authenticated user)."""
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.completed = toggle_data.completed
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)
    return task_to_response(task)


@router.delete("/{task_id}", status_code=204)
def delete_task(
    task_id: int,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    """Delete a task (only if owned by authenticated user)."""
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    session.delete(task)
    session.commit()
    return None
