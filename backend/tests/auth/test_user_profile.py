import pytest
from flask import Flask
from backend.app import create_app

@pytest.fixture
def app() -> Flask:
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    return app

@pytest.fixture
def client(app: Flask):
    return app.test_client()

def test_profile_update(client):
    client.post('/auth/register', json={
        "email": "profile.update@example.com",
        "password": "Password1!"
    })

    response = client.put('/auth/profile', json={
        "email": "profile.update@example.com",
        "name": "New Name",
        "phone": "1234567890"
    })
    assert response.status_code == 200
    assert response.get_json() == {
        "message": "Profile updated successfully",
        "user": {
            "email": "profile.update@example.com",
            "name": "New Name",
            "phone": "1234567890"
        }
    }

def test_profile_update_unregistered_email(client):
    response = client.put('/auth/profile', json={
        "email": "unregistered@example.com",
        "name": "Name",
        "phone": "1234567890"
    })
    assert response.status_code == 400
    assert response.get_json() == {"error": "Email not registered"}