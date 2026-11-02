#======= Pydantic Schemas for Student Validation ==============

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from enum import Enum
import re


class StudentStatus(str, Enum):
    active = "active"
    inactive = "inactive"
    graduated = "graduated"


class StudentBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: str = Field(..., min_length=5, max_length=100)
    programme: str = Field(..., min_length=2, max_length=100)
    level: int = Field(..., ge=100, le=600)
    gpa: Optional[float] = Field(None, ge=0.0, le=5.0)
    status: StudentStatus = Field(default=StudentStatus.active)

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, v):
            raise ValueError("Invalid email address format")
        return v.lower()

    @field_validator("first_name", "last_name")
    @classmethod
    def validate_names(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Name cannot be blank")
        return v.strip().title()


class StudentCreate(StudentBase):
    pass


class StudentUpdate(StudentBase):
    pass


class StudentPatch(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    email: Optional[str] = Field(None, min_length=5, max_length=100)
    programme: Optional[str] = Field(None, min_length=2, max_length=100)
    level: Optional[int] = Field(None, ge=100, le=600)
    gpa: Optional[float] = Field(None, ge=0.0, le=5.0)
    status: Optional[StudentStatus] = None

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, v):
            raise ValueError("Invalid email address format")
        return v.lower()


class StudentResponse(StudentBase):
    id: int


class StudentListResponse(BaseModel):
    total: int
    page: int
    limit: int
    students: List[StudentResponse]