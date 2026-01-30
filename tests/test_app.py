import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]

def test_signup_for_activity():
    # Use a unique email to avoid duplicate error
    email = "pytest_signup@mergington.edu"
    response = client.post(f"/activities/Chess%20Club/signup?email={email}")
    assert response.status_code == 200
    data = response.json()
    assert "Signed up" in data["message"]
    # Try signing up again, should fail
    response2 = client.post(f"/activities/Chess%20Club/signup?email={email}")
    assert response2.status_code == 400
    assert "already signed up" in response2.json()["detail"]

def test_signup_activity_not_found():
    response = client.post("/activities/Nonexistent/signup?email=someone@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

def test_unregister_participant():
    # First, sign up a test user
    email = "pytest_unregister@mergington.edu"
    client.post(f"/activities/Basketball/signup?email={email}")
    # Now, unregister
    response = client.delete(f"/activities/Basketball/unregister?email={email}")
    assert response.status_code == 200
    assert "Unregistered" in response.json()["message"]
    # Try again, should fail
    response2 = client.delete(f"/activities/Basketball/unregister?email={email}")
    assert response2.status_code == 400
    assert "not registered" in response2.json()["detail"]
