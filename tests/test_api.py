#======= Automated Test Suite for Student Management API ==============

import pytest
from fastapi.testclient import TestClient
from app.main import app, API_KEY
from app.store import store

client = TestClient(app)
HEADERS = {"X-API-Key": API_KEY}

SAMPLE = {
    "first_name": "Adewale",
    "last_name": "Ogunleye",
    "email": "adewale.ogunleye@gmail.com",
    "programme": "Computer Science",
    "level": 300,
    "gpa": 3.75,
    "status": "active",
}


@pytest.fixture(autouse=True)
def _reset():
    store.reset()
    yield
    store.reset()


#======= POST /students Tests ==============
class TestCreate:
    def test_create_success(self):
        r = client.post("/students", json=SAMPLE, headers=HEADERS)
        assert r.status_code == 201
        body = r.json()
        assert body["id"] == 1
        assert body["first_name"] == "Adewale"
        assert body["email"] == "adewale.ogunleye@gmail.com"

    def test_create_missing_field(self):
        r = client.post("/students", json={"first_name": "Adewale"}, headers=HEADERS)
        assert r.status_code == 422

    def test_create_invalid_email(self):
        r = client.post("/students", json={**SAMPLE, "email": "not-an-email"}, headers=HEADERS)
        assert r.status_code == 422

    def test_create_level_out_of_range(self):
        r = client.post("/students", json={**SAMPLE, "level": 999}, headers=HEADERS)
        assert r.status_code == 422

    def test_create_duplicate_email(self):
        client.post("/students", json=SAMPLE, headers=HEADERS)
        r = client.post("/students", json=SAMPLE, headers=HEADERS)
        assert r.status_code == 409

    def test_create_no_api_key(self):
        r = client.post("/students", json=SAMPLE)
        assert r.status_code == 401


#======= GET /students Tests ==============
class TestList:
    def test_list_empty(self):
        r = client.get("/students", headers=HEADERS)
        assert r.status_code == 200
        assert r.json()["total"] == 0

    def test_list_with_data(self):
        client.post("/students", json=SAMPLE, headers=HEADERS)
        r = client.get("/students", headers=HEADERS)
        assert r.json()["total"] == 1

    def test_list_filter_programme(self):
        client.post("/students", json=SAMPLE, headers=HEADERS)
        other = {**SAMPLE, "email": "temitope.balogun@gmail.com", "programme": "Medicine", "first_name": "Temitope", "last_name": "Balogun"}
        client.post("/students", json=other, headers=HEADERS)
        r = client.get("/students?programme=Medicine", headers=HEADERS)
        assert r.json()["total"] == 1

    def test_list_pagination(self):
        for i in range(5):
            client.post("/students", json={**SAMPLE, "email": f"student{i}@gmail.com"}, headers=HEADERS)
        r = client.get("/students?page=1&limit=2", headers=HEADERS)
        d = r.json()
        assert d["total"] == 5
        assert len(d["students"]) == 2


#======= GET /students/{id} Tests ==============
class TestGetOne:
    def test_get_found(self):
        sid = client.post("/students", json=SAMPLE, headers=HEADERS).json()["id"]
        r = client.get(f"/students/{sid}", headers=HEADERS)
        assert r.status_code == 200
        assert r.json()["last_name"] == "Ogunleye"

    def test_get_not_found(self):
        r = client.get("/students/999", headers=HEADERS)
        assert r.status_code == 404


#======= PUT /students/{id} Tests ==============
class TestPut:
    def test_put_success(self):
        sid = client.post("/students", json=SAMPLE, headers=HEADERS).json()["id"]
        updated = {**SAMPLE, "first_name": "Oluwaseun", "level": 400}
        r = client.put(f"/students/{sid}", json=updated, headers=HEADERS)
        assert r.status_code == 200
        assert r.json()["first_name"] == "Oluwaseun"
        assert r.json()["level"] == 400

    def test_put_not_found(self):
        r = client.put("/students/999", json=SAMPLE, headers=HEADERS)
        assert r.status_code == 404


#======= PATCH /students/{id} Tests ==============
class TestPatch:
    def test_patch_success(self):
        sid = client.post("/students", json=SAMPLE, headers=HEADERS).json()["id"]
        r = client.patch(f"/students/{sid}", json={"gpa": 4.5}, headers=HEADERS)
        assert r.status_code == 200
        assert r.json()["gpa"] == 4.5
        assert r.json()["first_name"] == "Adewale"

    def test_patch_not_found(self):
        r = client.patch("/students/999", json={"gpa": 4.0}, headers=HEADERS)
        assert r.status_code == 404


#======= DELETE /students/{id} Tests ==============
class TestDelete:
    def test_delete_success(self):
        sid = client.post("/students", json=SAMPLE, headers=HEADERS).json()["id"]
        r = client.delete(f"/students/{sid}", headers=HEADERS)
        assert r.status_code == 200
        assert client.get(f"/students/{sid}", headers=HEADERS).status_code == 404

    def test_delete_not_found(self):
        r = client.delete("/students/999", headers=HEADERS)
        assert r.status_code == 404