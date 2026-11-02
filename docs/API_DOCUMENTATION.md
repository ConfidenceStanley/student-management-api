Endpoints
4.1 POST /students — Create a Student
Request:
{
  "first_name": "Adewale",
  "last_name": "Ogunleye",
  "email": "adewaleogunleye@gmail.com",
  "programme": "Computer Science",
  "level": 300,
  "gpa": 3.75,
  "status": "active"
}

Success Response — 201 Created:
{
  "id": 1,
  "first_name": "Adewale",
  "last_name": "Ogunleye",
  "email": "adewale.ogunleye@gmail.com",
  "programme": "Computer Science",
  "level": 300,
  "gpa": 3.75,
  "status": "active"
}

Error Responses:
Code	Condition
403	Missing or invalid API key
409	Email already exists
422	Validation failure (missing fields, bad email, level out of range)


4.2 GET /students — List All Students
Query Parameters:
Parameter	Type	Default	Description
programme	string	—	Filter by programme name
status	string	—	Filter: active, inactive, graduated
page	int	1	Page number (≥ 1)
limit	int	10	Items per page (1–100)

Success Response — 200 OK:
{
  "total": 2,
  "page": 1,
  "limit": 10,
  "students": [
    {
      "id": 1,
      "first_name": "Adewale",
      "last_name": "Ogunleye",
      "email": "adewale.ogunleye@gmail.com",
      "programme": "Computer Science",
      "level": 300,
      "gpa": 3.75,
      "status": "active"
    }
  ]
}

4.3 GET /students/{id} — Retrieve One Student
Success Response — 200 OK: Returns a single student object.
Error: 404 Not Found if the ID does not exist.

4.4 PUT /students/{id} — Full Update
Replaces all fields. The request body must include every required field.
Request:
{
  "first_name": "Oluwaseun",
  "last_name": "Adebayo",
  "email": "oluwaseun.adebayo@gmail.com",
  "programme": "Software Engineering",
  "level": 400,
  "gpa": 4.10,
  "status": "active"
}
Error Responses: 403, 404, 409, 422

4.5 PATCH /students/{id} — Partial Update
Updates only the fields included in the request body.
Request:
{
  "gpa": 4.50,
  "level": 500
}
Success Response — 200 OK: Returns the full updated student record with unchanged fields preserved.
Error Responses: 403, 404, 409, 422

4.6 DELETE /students/{id} — Delete a Student
Success Response — 200 OK:
{
  "message": "Student 1 deleted successfully",
  "status": "success"
}
Error: 404 Not Found if the ID does not exist.
