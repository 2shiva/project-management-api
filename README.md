# Project Management API

A REST API built with **FastAPI** for managing projects and tasks.

## Features

- User Registration & Login (JWT Authentication)
- Create, Update, Delete Projects
- Create, Update, Delete Tasks
- Team Member Management
- Comments on Tasks
- Dashboard API
- File Upload
- Swagger API Documentation

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- JWT Authentication
- Alembic

## Installation

Clone the repository

```bash
git clone git@github.com:2shiva/project-management-api.git
```

Go to the project folder

```bash
cd project-management-api
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the virtual environment

**macOS/Linux**

```bash
source venv/bin/activate
```

**Windows**

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the server

```bash
uvicorn app.main:app --reload
```

## API Documentation

Swagger UI

```
http://127.0.0.1:8000/docs
```

ReDoc

```
http://127.0.0.1:8000/redoc
```

## Project Structure

```
project-management-api
│
├── app/
├── alembic/
├── requirements.txt
├── README.md
└── .gitignore
```

## Author

**Shiva**

GitHub: https://github.com/2shiva