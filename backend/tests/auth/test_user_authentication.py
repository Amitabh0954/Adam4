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

def test_user_login(client):
    client.post('/auth/register', json={
        "email": "login.test@example.com",
        "password": "Password1!"
    })

    response = client.post('/auth/login', json={
        "email": "login.test@example.com",
        "password": "Password1!"
    })
    assert response.status_code == 200
    assert response.get_json() == {"message": "Login successful"}

def test_user_login_with_invalid_password(client):
    client.post('/auth/register', json={
        "email": "invalid.password@example.com",
        "password": "Password1!"
    })

    response = client.post('/auth/login', json={
        "email": "invalid.password@example.com",
        "password": "WrongPassword!"
    })
    assert response.status_code == 401
    assert response.get_json() == {"error": "Invalid email or password"}

def test_user_login_attempts_limit(client):
    client.post('/auth/register', json={
        "email": "attempt.limit@example.com",
        "password": "Password1!"
    })

    for _ in range(4):
        client.post('/auth/login', json={
            "email": "attempt.limit@example.com",
            "password": "WrongPassword!"
        })

    response = client.post('/auth/login', json={
        "email": "attempt.limit@example.com",
        "password": "Password1!"
    })
    assert response.status_code == 401
    assert response.get_json() == {"error": "Invalid email or password"}