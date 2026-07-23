from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app import models
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/audit-logs",
    tags=["Audit Logs"]
)


# Get all audit logs
@router.get("/")
def get_all_audit_logs(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return db.query(models.AuditLog).all()


# Get audit logs for an entity
@router.get("/{entity_type}/{entity_id}")
def get_entity_audit_logs(
    entity_type: str,
    entity_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return db.query(models.AuditLog).filter(
        models.AuditLog.entity_type == entity_type,
        models.AuditLog.entity_id == entity_id
    ).all()