# Student Management REST API

## Purpose
RESTful API for managing university student records with full CRUD,
input validation, API key authentication, filtering and pagination.

## Tech Stack
- Python 3.11+ / FastAPI / Pydantic v2 / Uvicorn
- Testing: pytest + httpx

## Quick Start

git clone https://github.com/ConfidenceStanley/student-management-api.git
cd student-management-api
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

Open http://127.0.0.1:8000/docs for Swagger UI

Authentication

All endpoints require: X-API-Key: sm-api-2025-secure-key

Endpoints
Method	Path	Description
POST	/students	Create student (201)
GET	/students	List + filter + paginate (200)
GET	/students/{id}	Get one student (200/404)
PUT	/students/{id}	Full update (200/404)
PATCH	/students/{id}	Partial update (200/404)
DELETE	/students/{id}	Delete student (200/404)