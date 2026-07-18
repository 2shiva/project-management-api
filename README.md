# Project Management API

## Overview
A RESTful Project Management API built using FastAPI. It supports user authentication, project management, task management, comments, file uploads, activity tracking, and role-based access control.

## Technologies Used

- Python
- FastAPI
- SQLAlchemy
- SQLite
- JWT Authentication
- OAuth2
- Pydantic
- Uvicorn

## Features

### Authentication
- User Signup
- User Login
- JWT Authentication

### Projects
- Create Project
- View Projects
- Update Project
- Delete Project

### Members
- Add Members
- View Members
- Remove Members

### Tasks
- Create Task
- View Tasks
- Update Task
- Delete Task

### Dashboard
- Project Dashboard

### Activity
- Activity Tracking

### Comments
- Add Comment
- View Comments

### File Upload
- Upload Files
- View Uploaded Files
- Delete Uploaded Files

## Run Project

Create virtual environment

```bash
python3 -m venv venv
```

Activate

```bash
source venv/bin/activate
```

Install packages

```bash
pip install -r requirements.txt
```

Run

```bash
uvicorn app.main:app --reload
```

Swagger

```
http://127.0.0.1:8000/docs
```