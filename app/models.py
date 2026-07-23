from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base



# User Table
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)

    created_projects = relationship("Project", back_populates="creator")
    assigned_tasks = relationship("Task", back_populates="assignee")



# Project Table

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    created_by = Column(Integer, ForeignKey("users.id"))

    creator = relationship("User", back_populates="created_projects")

    tasks = relationship("Task", back_populates="project")
    members = relationship("ProjectMember", back_populates="project")



# Project Members Table

class ProjectMember(Base):
    __tablename__ = "project_members"

    id = Column(Integer, primary_key=True, index=True)

    project_id = Column(Integer, ForeignKey("projects.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    project = relationship("Project", back_populates="members")
    user = relationship("User")



# Task Table

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)
    description = Column(Text)

    status = Column(String, default="Pending")
    priority = Column(String, default="Medium")

    due_date = Column(DateTime)

    assigned_to = Column(Integer, ForeignKey("users.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))

    assignee = relationship("User", back_populates="assigned_tasks")
    project = relationship("Project", back_populates="tasks")



# Activity Log Table

class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    action = Column(String, nullable=False)

    entity_type = Column(String, nullable=False)

    entity_id = Column(Integer, nullable=False)

    description = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")



# Comment Table

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)

    comment = Column(Text, nullable=False)

    task_id = Column(Integer, ForeignKey("tasks.id"))

    user_id = Column(Integer, ForeignKey("users.id"))

    created_at = Column(DateTime, default=datetime.utcnow)

    task = relationship("Task")
    user = relationship("User")



# File Upload Table

class FileUpload(Base):
    __tablename__ = "file_uploads"

    id = Column(Integer, primary_key=True, index=True)

    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)

    filename = Column(String, nullable=False)

    file_path = Column(String, nullable=False)

    uploaded_by = Column(Integer, ForeignKey("users.id"))

    created_at = Column(DateTime, default=datetime.utcnow)

    task = relationship("Task")
    user = relationship("User")



# Notification Table

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    title = Column(String, nullable=False)

    message = Column(String, nullable=False)

    is_read = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")

# Audit Log Table

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)

    entity_type = Column(String, nullable=False)

    entity_id = Column(Integer, nullable=False)

    field_name = Column(String, nullable=False)

    old_value = Column(String)

    new_value = Column(String)

    changed_by = Column(Integer, ForeignKey("users.id"))

    changed_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")