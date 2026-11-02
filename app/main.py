#======= Student Management REST API — Main Application ==============

from fastapi import FastAPI, HTTPException, Query, Depends, Security
from fastapi.security import APIKeyHeader
from typing import Optional

from app.models import (
    StudentCreate,
    StudentUpdate,
    StudentPatch,
    StudentResponse,
    StudentListResponse,
)
from app.store import store

API_KEY = "sm-api-2025-secure-key"
api_key_header = APIKeyHeader(name="X-API-Key")


def verify_api_key(key: str = Security(api_key_header)):
    if key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid or missing API key")
    return key


app = FastAPI(
    title="Student Management API",
    description="RESTful API for managing university student records with authentication, validation, filtering and pagination.",
    version="1.0.0",
)


@app.get("/", tags=["Health"])
def root():
    return {
        "api": "Student Management API",
        "version": "1.0.0",
        "docs": "/docs",
    }


#======= Create Student ==============
@app.post(
    "/students",
    response_model=StudentResponse,
    status_code=201,
    tags=["Students"],
    dependencies=[Depends(verify_api_key)],
)
def create_student(student: StudentCreate):
    if store.email_exists(student.email):
        raise HTTPException(status_code=409, detail="A student with this email already exists")
    return store.create(student)


#======= List Students ==============
@app.get(
    "/students",
    response_model=StudentListResponse,
    tags=["Students"],
    dependencies=[Depends(verify_api_key)],
)
def list_students(
    programme: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
):
    return store.get_all(programme=programme, status=status, page=page, limit=limit)


#======= Get Single Student ==============
@app.get(
    "/students/{student_id}",
    response_model=StudentResponse,
    tags=["Students"],
    dependencies=[Depends(verify_api_key)],
)
def get_student(student_id: int):
    student = store.get_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail=f"Student with ID {student_id} not found")
    return student


#======= Full Update Student ==============
@app.put(
    "/students/{student_id}",
    response_model=StudentResponse,
    tags=["Students"],
    dependencies=[Depends(verify_api_key)],
)
def update_student(student_id: int, student: StudentUpdate):
    if store.email_exists(student.email, exclude_id=student_id):
        raise HTTPException(status_code=409, detail="A student with this email already exists")
    updated = store.update(student_id, student)
    if not updated:
        raise HTTPException(status_code=404, detail=f"Student with ID {student_id} not found")
    return updated


#======= Partial Update Student ==============
@app.patch(
    "/students/{student_id}",
    response_model=StudentResponse,
    tags=["Students"],
    dependencies=[Depends(verify_api_key)],
)
def patch_student(student_id: int, updates: StudentPatch):
    if updates.email and store.email_exists(updates.email, exclude_id=student_id):
        raise HTTPException(status_code=409, detail="A student with this email already exists")
    updated = store.patch(student_id, updates)
    if not updated:
        raise HTTPException(status_code=404, detail=f"Student with ID {student_id} not found")
    return updated


#======= Delete Student ==============
@app.delete(
    "/students/{student_id}",
    tags=["Students"],
    dependencies=[Depends(verify_api_key)],
)
def delete_student(student_id: int):
    if not store.delete(student_id):
        raise HTTPException(status_code=404, detail=f"Student with ID {student_id} not found")
    return {"message": f"Student {student_id} deleted successfully", "status": "success"}