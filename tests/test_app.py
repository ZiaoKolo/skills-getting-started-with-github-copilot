import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_signup_and_duplicate():
    # Inscription
    response = client.post("/activities/Chess/signup?email=test1@mergington.edu")
    assert response.status_code == 200
    # Double inscription
    response2 = client.post("/activities/Chess/signup?email=test1@mergington.edu")
    assert response2.status_code == 400
    assert "already registered" in response2.json()["detail"].lower()

def test_delete_signup():
    # Inscription
    client.post("/activities/Drama/signup?email=test2@mergington.edu")
    # Désinscription
    response = client.delete("/activities/Drama/signup?email=test2@mergington.edu")
    assert response.status_code == 200
    # Désinscription d'un non-inscrit
    response2 = client.delete("/activities/Drama/signup?email=test2@mergington.edu")
    assert response2.status_code == 400
    assert "not registered" in response2.json()["detail"].lower()
