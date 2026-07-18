from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/projects",
    tags=["Project Members"]
)


# Add Member to Project
@router.post("/{project_id}/members", response_model=schemas.ProjectMemberResponse)
def add_member(
    project_id: int,
    member: schemas.ProjectMemberCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    project = db.query(models.Project).filter(
        models.Project.id == project_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    user = db.query(models.User).filter(
        models.User.id == member.user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    existing = db.query(models.ProjectMember).filter(
        models.ProjectMember.project_id == project_id,
        models.ProjectMember.user_id == member.user_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="User is already a member"
        )

    new_member = models.ProjectMember(
        project_id=project_id,
        user_id=member.user_id
    )

    db.add(new_member)
    db.commit()
    db.refresh(new_member)

    return new_member


# Get All Members of a Project
@router.get("/{project_id}/members", response_model=list[schemas.ProjectMemberResponse])
def get_project_members(
    project_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    members = db.query(models.ProjectMember).filter(
        models.ProjectMember.project_id == project_id
    ).all()

    return members


# Remove Member from Project
@router.delete("/{project_id}/members/{user_id}")
def remove_member(
    project_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    member = db.query(models.ProjectMember).filter(
        models.ProjectMember.project_id == project_id,
        models.ProjectMember.user_id == user_id
    ).first()

    if not member:
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )

    db.delete(member)
    db.commit()

    return {
        "message": "Member removed successfully"
    }