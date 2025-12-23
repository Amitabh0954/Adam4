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

def test_register_user(client):
    response = client.post('/auth/register', json={
        "email": "test@example.com",
        "password": "Password1!"
    })
    assert response.status_code == 201
    assert response.get_json() == {"message": "User registered successfully"}

def test_register_user_with_existing_email(client):
    client.post('/auth/register', json={
        "email": "test@example.com",
        "password": "Password1!"
    })

    response = client.post('/auth/register', json={
        "email": "test@example.com",
        "password": "Password1!"
    })
    assert response.status_code == 400
    assert response.get_json() == {"error": "Email must be unique"}

def test_register_user_with_weak_password(client):
    response = client.post('/auth/register', json={
        "email": "test@example.com",
        "password": "weakpass"
    })
    assert response.status_code == 400
    assert response.get_json() == {"error": "Password must meet security criteria"}