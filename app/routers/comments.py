from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/comments",
    tags=["Comments"]
)


# Create Comment
@router.post("/{task_id}", response_model=schemas.CommentResponse)
def create_comment(
    task_id: int,
    comment: schemas.CommentCreate,
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

    new_comment = models.Comment(
        comment=comment.comment,
        task_id=task_id,
        user_id=current_user["user_id"]
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment


# Get Comments for a Task
@router.get("/{task_id}", response_model=list[schemas.CommentResponse])
def get_comments(
    task_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return db.query(models.Comment).filter(
        models.Comment.task_id == task_id
    ).all()