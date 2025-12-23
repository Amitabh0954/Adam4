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

def test_password_reset(client):
    client.post('/auth/register', json={
        "email": "reset.test@example.com",
        "password": "Password1!"
    })

    response = client.post('/auth/reset_password', json={
        "email": "reset.test@example.com"
    })
    assert response.status_code == 200
    assert response.get_json() == {"message": "Password reset link sent to reset.test@example.com"}

def test_password_reset_unregistered_email(client):
    response = client.post('/auth/reset_password', json={
        "email": "unregistered@example.com"
    })
    assert response.status_code == 400
    assert response.get_json() == {"error": "Email not registered"}