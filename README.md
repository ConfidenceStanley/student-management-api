# Student Management REST API

RESTful API for managing university student records with full CRUD, input validation, API key authentication, filtering and pagination.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.12 |
| Framework | FastAPI |
| Validation | Pydantic v2 |
| Server | Uvicorn |
| Testing | pytest + httpx |

---

## Quick Start

```bash
git clone https://github.com/ConfidenceStanley/student-management-api.git
cd student-management-api
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for Swagger UI.

---

## Authentication

All `/students` endpoints require an API key in the request header:

```
X-API-Key: sm-api-2025-secure-key
```

| Scenario | Status Code |
|----------|-------------|
| Valid key | 200 / 201 |
| Missing key | 401 Unauthorized |
| Invalid key | 403 Forbidden |

---

## Endpoints

| Method | Path | Description | Status Codes |
|--------|------|-------------|--------------|
| `POST` | `/students` | Create a new student | 201, 401, 409, 422 |
| `GET` | `/students` | List all students (filter + paginate) | 200, 401 |
| `GET` | `/students/{id}` | Retrieve one student by ID | 200, 401, 404 |
| `PUT` | `/students/{id}` | Full update (all fields required) | 200, 401, 404, 409, 422 |
| `PATCH` | `/students/{id}` | Partial update (only sent fields) | 200, 401, 404, 409, 422 |
| `DELETE` | `/students/{id}` | Delete a student | 200, 401, 404 |

### Query Parameters (GET /students)

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `programme` | string | — | Filter by programme name |
| `status` | string | — | Filter by status (active, inactive, graduated) |
| `page` | int | 1 | Page number (≥ 1) |
| `limit` | int | 10 | Items per page (1–100) |

---

## Example Request

```json
POST /students
Headers: X-API-Key: sm-api-2025-secure-key

{
  "first_name": "Adewale",
  "last_name": "Ogunleye",
  "email": "adewale.ogunleye@gmail.com",
  "programme": "Computer Science",
  "level": 300,
  "gpa": 3.75,
  "status": "active"
}
```

---

## Run Tests

```bash
pytest tests/ -v
```

---

## Project Structure

```
student-management-api/
├── app/
│   ├── __init__.py
│   ├── main.py          # Routes and authentication
│   ├── models.py        # Pydantic schemas and validators
│   └── store.py         # Data access layer (CRUD)
├── tests/
│   ├── __init__.py
│   └── test_api.py      # 18 automated test cases
├── docs/
│   ├── API_DOCUMENTATION.md
├── requirements.txt
├── README.md
└── .gitignore
```

