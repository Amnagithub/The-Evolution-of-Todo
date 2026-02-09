"""Task CRUD endpoints with JWT authentication."""
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
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
        priority=task.priority,
        created_at=task.created_at,
        updated_at=task.updated_at,
    )


@router.get("", response_model=List[TaskResponse])
def list_tasks(
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session),
    search: Optional[str] = Query(None, description="Search in title and description"),
    priority: Optional[str] = Query(None, description="Filter by priority (low, medium, high)"),
    sort_by: Optional[str] = Query("created_at", description="Sort by field (created_at, title, priority)"),
    sort_order: Optional[str] = Query("desc", description="Sort order (asc, desc)"),
):
    """List all tasks for the authenticated user with search, filter, and sort options."""
    statement = select(Task).where(Task.user_id == user_id)

    # Apply search filter
    if search:
        search_term = f"%{search}%"
        statement = statement.where(
            (Task.title.ilike(search_term)) | (Task.description.ilike(search_term))
        )

    # Apply priority filter
    if priority and priority in ["low", "medium", "high"]:
        statement = statement.where(Task.priority == priority)

    # Apply sorting
    if sort_by == "title":
        order_column = Task.title
    elif sort_by == "priority":
        # Custom priority order: high > medium > low
        from sqlalchemy import case
        priority_order = case(
            (Task.priority == "high", 1),
            (Task.priority == "medium", 2),
            (Task.priority == "low", 3),
            else_=4
        )
        order_column = priority_order
    else:
        order_column = Task.created_at

    if sort_order == "asc":
        statement = statement.order_by(order_column.asc() if hasattr(order_column, 'asc') else order_column)
    else:
        statement = statement.order_by(order_column.desc() if hasattr(order_column, 'desc') else order_column)

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

    # Validate priority
    priority = task_data.priority or "medium"
    if priority not in ["low", "medium", "high"]:
        raise HTTPException(status_code=422, detail="Priority must be low, medium, or high")

    task = Task(
        title=task_data.title.strip(),
        description=task_data.description,
        priority=priority,
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

    if task_data.priority is not None:
        if task_data.priority not in ["low", "medium", "high"]:
            raise HTTPException(status_code=422, detail="Priority must be low, medium, or high")
        task.priority = task_data.priority

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
