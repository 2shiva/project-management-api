from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


# Create Task
@router.post("/", response_model=schemas.TaskResponse)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    project = db.query(models.Project).filter(
        models.Project.id == task.project_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    user = db.query(models.User).filter(
        models.User.id == task.assigned_to
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Assigned user not found"
        )

    new_task = models.Task(
        title=task.title,
        description=task.description,
        priority=task.priority,
        due_date=task.due_date,
        assigned_to=task.assigned_to,
        project_id=task.project_id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    # Activity Log
    activity = models.ActivityLog(
        user_id=current_user["user_id"],
        action="Task Created",
        entity_type="Task",
        entity_id=new_task.id,
        description=f"Created task '{new_task.title}'"
    )

    db.add(activity)

    # Notification
    notification = models.Notification(
        user_id=task.assigned_to,
        title="New Task Assigned",
        message=f"You have been assigned the task '{new_task.title}'."
    )

    db.add(notification)

    db.commit()

    return new_task


# Get All Tasks
@router.get("/", response_model=list[schemas.TaskResponse])
def get_tasks(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return db.query(models.Task).all()


# Get Single Task
@router.get("/{task_id}", response_model=schemas.TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    task = db.query(models.Task).filter(
        models.Task.id == task_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task


# Update Task
@router.put("/{task_id}", response_model=schemas.TaskResponse)
def update_task(
    task_id: int,
    task: schemas.TaskUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    db_task = db.query(models.Task).filter(
        models.Task.id == task_id
    ).first()

    if not db_task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    # Save old values
    old_status = db_task.status

    # Update task
    db_task.title = task.title
    db_task.description = task.description
    db_task.status = task.status
    db_task.priority = task.priority
    db_task.due_date = task.due_date
    db_task.assigned_to = task.assigned_to

    db.commit()
    db.refresh(db_task)

    # Activity Log
    activity = models.ActivityLog(
        user_id=current_user["user_id"],
        action="Task Updated",
        entity_type="Task",
        entity_id=db_task.id,
        description=f"Updated task '{db_task.title}'"
    )
    db.add(activity)

    # Audit Log (Status Change)
    if old_status != db_task.status:
        audit = models.AuditLog(
            entity_type="Task",
            entity_id=db_task.id,
            field_name="status",
            old_value=old_status,
            new_value=db_task.status,
            changed_by=current_user["user_id"]
        )
        db.add(audit)

    db.commit()

    return db_task


# Delete Task
@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    task = db.query(models.Task).filter(
        models.Task.id == task_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()

    return {
        "message": "Task deleted successfully"
    }