from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas
from app.dependencies import get_current_user, manager_required

router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)


# Create Project
@router.post("/", response_model=schemas.ProjectResponse)
def create_project(
    project: schemas.ProjectCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    new_project = models.Project(
        name=project.name,
        description=project.description,
        created_by=current_user["user_id"]
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    # Activity Log
    activity = models.ActivityLog(
        user_id=current_user["user_id"],
        action=f"Created project: {new_project.name}",
        entity_type="Project",
        entity_id=new_project.id,
        description=f"Project '{new_project.name}' was created."
    )

    db.add(activity)
    db.commit()

    return new_project


# Get All Projects
@router.get("/", response_model=list[schemas.ProjectResponse])
def get_projects(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return db.query(models.Project).all()


# Get Single Project
@router.get("/{project_id}", response_model=schemas.ProjectResponse)
def get_project(
    project_id: int,
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

    return project


# Update Project
@router.put("/{project_id}", response_model=schemas.ProjectResponse)
def update_project(
    project_id: int,
    project: schemas.ProjectUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    db_project = db.query(models.Project).filter(
        models.Project.id == project_id
    ).first()

    if not db_project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    if db_project.created_by != current_user["user_id"]:
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to update this project"
        )

    db_project.name = project.name
    db_project.description = project.description

    db.commit()
    db.refresh(db_project)

    return db_project


# Delete Project
@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(manager_required)
):
    project = db.query(models.Project).filter(
        models.Project.id == project_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    db.delete(project)
    db.commit()

    return {
        "message": "Project deleted successfully"
    }