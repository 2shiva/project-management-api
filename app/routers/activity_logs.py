from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app import models
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/activities",
    tags=["Activity Logs"]
)


# Get all activities
@router.get("/")
def get_all_activities(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return db.query(models.ActivityLog).all()


# Get activities of one user
@router.get("/user/{user_id}")
def get_user_activities(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return db.query(models.ActivityLog).filter(
        models.ActivityLog.user_id == user_id
    ).all()


# Get project activities
@router.get("/project/{project_id}")
def get_project_activities(
    project_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return db.query(models.ActivityLog).filter(
        models.ActivityLog.entity_type == "Task",
        models.ActivityLog.entity_id == project_id
    ).all()