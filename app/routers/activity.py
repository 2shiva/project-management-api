from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app import models
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/activity",
    tags=["Activity"]
)


@router.get("/")
def get_activity(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    activities = db.query(models.ActivityLog).all()

    return activities