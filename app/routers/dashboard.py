from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app import models
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/")
def get_dashboard(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    total_projects = db.query(models.Project).count()

    total_tasks = db.query(models.Task).count()

    completed_tasks = db.query(models.Task).filter(
        models.Task.status == "Completed"
    ).count()

    pending_tasks = db.query(models.Task).filter(
        models.Task.status == "Pending"
    ).count()

    in_progress_tasks = db.query(models.Task).filter(
        models.Task.status == "In Progress"
    ).count()

    return {
        "total_projects": total_projects,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "in_progress_tasks": in_progress_tasks
    }