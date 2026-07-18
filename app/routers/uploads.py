from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
import shutil
import os

from app.database import get_db
from app import models
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/uploads",
    tags=["Uploads"]
)


@router.post("/{task_id}")
def upload_file(
    task_id: int,
    file: UploadFile = File(...),
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

    file_path = os.path.join("uploads", file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_file = models.FileUpload(
        task_id=task_id,
        filename=file.filename,
        file_path=file_path,
        uploaded_by=current_user["user_id"]
    )

    db.add(new_file)
    db.commit()
    db.refresh(new_file)

    return {
        "message": "File uploaded successfully",
        "file_id": new_file.id,
        "filename": new_file.filename,
        "path": new_file.file_path
    }


@router.get("/{task_id}")
def get_task_files(
    task_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    files = db.query(models.FileUpload).filter(
        models.FileUpload.task_id == task_id
    ).all()

    return files


@router.delete("/file/{file_id}")
def delete_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    file = db.query(models.FileUpload).filter(
        models.FileUpload.id == file_id
    ).first()

    if not file:
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    if os.path.exists(file.file_path):
        os.remove(file.file_path)

    db.delete(file)
    db.commit()

    return {
        "message": "File deleted successfully"
    }