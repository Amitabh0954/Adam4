import pytest
from flask import Flask, session
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
        "email": "testuser@example.com",
        "password": "SecureP@ss123"
    })
    assert response.status_code == 201
    assert response.get_json() == {"message": "User registered successfully"}

def test_register_user_with_existing_email(client):
    client.post('/auth/register', json={
        "email": "testuser@example.com",
        "password": "SecureP@ss123"
    })
    response = client.post('/auth/register', json={
        "email": "testuser@example.com",
        "password": "AnotherP@ss123"
    })
    assert response.status_code == 400
    assert response.get_json() == {"error": "Email is already registered"}

def test_register_user_with_invalid_password(client):
    response = client.post('/auth/register', json={
        "email": "testuser@example.com",
        "password": "short"
    })
    assert response.status_code == 400
    assert response.get_json() == {"error": "Password does not meet security criteria"}

def test_login_user(client):
    client.post('/auth/register', json={
        "email": "testuser@example.com",
        "password": "SecureP@ss123"
    })
    response = client.post('/auth/login', json={
        "email": "testuser@example.com",
        "password": "SecureP@ss123"
    })
    assert response.status_code == 200
    assert response.get_json() == {"message": "Logged in successfully"}

def test_login_user_invalid_credentials(client):
    response = client.post('/auth/login', json={
        "email": "invalid@example.com",
        "password": "invalidpassword"
    })
    assert response.status_code == 401
    assert response.get_json() == {"error": "Invalid email or password"}

def test_logout_user(client):
    with client.session_transaction() as sess:
        sess['user_id'] = 'user_id'

    response = client.post('/auth/logout')
    assert response.status_code == 200
    assert response.get_json() == {"message": "Logged out successfully"}
    with client.session_transaction() as sess:
        assert 'user_id' not in sess

def test_request_password_reset(client):
    client.post('/auth/register', json={
        "email": "testuser@example.com",
        "password": "SecureP@ss123"
    })
    response = client.post('/auth/request_password_reset', json={
        "email": "testuser@example.com"
    })
    assert response.status_code == 200
    assert response.get_json() == {"message": "Password reset email sent"}

def test_reset_password(client):
    client.post('/auth/register', json={
        "email": "testuser@example.com",
        "password": "SecureP@ss123"
    })
    client.post('/auth/request_password_reset', json={
        "email": "testuser@example.com"
    })
    auth_service = AuthService()
    user = auth_service.auth_repository.get_user_by_email("testuser@example.com")
    token = user.reset_token

    response = client.post('/auth/reset_password', json={
        "token": token,
        "new_password": "NewSecureP@ss456"
    })
    assert response.status_code == 200
    assert response.get_json() == {"message": "Password reset successfully"}

    assert auth_service.verify_user("testuser@example.com", "NewSecureP@ss456")