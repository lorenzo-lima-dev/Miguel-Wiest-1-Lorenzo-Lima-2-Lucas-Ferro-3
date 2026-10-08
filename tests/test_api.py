import pytest
from fastapi.testclient import TestClient
from fastapi.main import app

client = TestClient(app)

def test_access_without_token():
    response = client.get("/predictions/1")
    assert response.status_code == 401

def test_bola_access_denied():
    login = client.post("/auth/token", data={"username": "user2", "password": "senha456"})
    token = login.json()["access_token"]
    response = client.get("/predictions/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404

def test_extra_fields_forbidden():
    login = client.post("/auth/token", data={"username": "user1", "password": "senha123"})
    token = login.json()["access_token"]
    payload = {"input_text": "Texto", "campo_hacker": "inject"}
    response = client.post("/predictions/", json=payload, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 422
