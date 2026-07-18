from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

from app.database import Base, engine
import app.routers.auth as auth
import app.routers.projects as projects
import app.routers.tasks as tasks
import app.routers.members as members
import app.routers.dashboard as dashboard
import app.routers.activity as activity
import app.routers.comments as comments
import app.routers.uploads as uploads

# Create database tables
Base.metadata.create_all(bind=engine)

# Create uploads folder if it doesn't exist
os.makedirs("uploads", exist_ok=True)

app = FastAPI(
    title="Project Management API"
)

# Register Routers
app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(tasks.router)
app.include_router(members.router)
app.include_router(dashboard.router)
app.include_router(activity.router)
app.include_router(comments.router)
app.include_router(uploads.router)

# Serve uploaded files
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


@app.get("/")
def home():
    return {
        "message": "Project Management API is running"
    }