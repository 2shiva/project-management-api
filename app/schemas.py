from datetime import datetime
from pydantic import BaseModel, EmailStr

# -----------------------
# User Schemas
# -----------------------
class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role: str


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# -----------------------
# JWT Token
# -----------------------
class Token(BaseModel):
    access_token: str
    token_type: str


# -----------------------
# Project Schemas
# -----------------------
class ProjectCreate(BaseModel):
    name: str
    description: str


class ProjectUpdate(BaseModel):
    name: str
    description: str


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str
    created_by: int
    created_at: datetime

    class Config:
        from_attributes = True


# -----------------------
# Task Schemas
# -----------------------
class TaskCreate(BaseModel):
    title: str
    description: str
    priority: str
    due_date: datetime
    assigned_to: int
    project_id: int


class TaskUpdate(BaseModel):
    title: str
    description: str
    status: str
    priority: str
    due_date: datetime
    assigned_to: int


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    status: str
    priority: str
    due_date: datetime
    assigned_to: int
    project_id: int

    class Config:
        from_attributes = True


# -----------------------
# Project Member Schemas
# -----------------------
class ProjectMemberCreate(BaseModel):
    user_id: int


class ProjectMemberResponse(BaseModel):
    id: int
    project_id: int
    user_id: int

    class Config:
        from_attributes = True
        
# -----------------------
# Comment Schemas
# -----------------------

class CommentCreate(BaseModel):
    comment: str


class CommentResponse(BaseModel):
    id: int
    comment: str
    task_id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True