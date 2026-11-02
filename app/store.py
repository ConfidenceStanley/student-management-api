#======= In-Memory Data Store and CRUD Operations ==============

from typing import Optional
from app.models import StudentCreate, StudentUpdate, StudentPatch


class StudentStore:

    def __init__(self):
        self._students: dict[int, dict] = {}
        self._next_id: int = 1

    def create(self, student: StudentCreate) -> dict:
        student_id = self._next_id
        self._next_id += 1
        record = {"id": student_id, **student.model_dump()}
        self._students[student_id] = record
        return record

    def get_all(
        self,
        programme: Optional[str] = None,
        status: Optional[str] = None,
        page: int = 1,
        limit: int = 10,
    ) -> dict:
        results = list(self._students.values())

        if programme:
            results = [
                s for s in results
                if s["programme"].lower() == programme.lower()
            ]
        if status:
            results = [
                s for s in results
                if s["status"] == status
            ]

        total = len(results)
        start = (page - 1) * limit
        end = start + limit

        return {
            "total": total,
            "page": page,
            "limit": limit,
            "students": results[start:end],
        }

    def get_by_id(self, student_id: int) -> Optional[dict]:
        return self._students.get(student_id)

    def update(self, student_id: int, student: StudentUpdate) -> Optional[dict]:
        if student_id not in self._students:
            return None
        self._students[student_id] = {
            "id": student_id, **student.model_dump()
        }
        return self._students[student_id]

    def patch(self, student_id: int, updates: StudentPatch) -> Optional[dict]:
        if student_id not in self._students:
            return None
        changed = updates.model_dump(exclude_unset=True)
        self._students[student_id].update(changed)
        return self._students[student_id]

    def delete(self, student_id: int) -> bool:
        if student_id not in self._students:
            return False
        del self._students[student_id]
        return True

    def email_exists(self, email: str, exclude_id: int | None = None) -> bool:
        for s in self._students.values():
            if s["id"] != exclude_id and s["email"] == email.lower():
                return True
        return False

    def reset(self):
        self._students.clear()
        self._next_id = 1


store = StudentStore()