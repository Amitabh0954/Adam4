import pytest
from backend.services.auth.auth_service import AuthService

@pytest.fixture
def auth_service() -> AuthService:
    return AuthService()

def test_is_email_taken(auth_service):
    auth_service.register_user("testuser@example.com", "SecureP@ss123")
    assert auth_service.is_email_taken("testuser@example.com") is True

def test_is_valid_password(auth_service):
    assert auth_service.is_valid_password("SecureP@ss123") is True
    assert auth_service.is_valid_password("short") is False
    assert auth_service.is_valid_password("nouppercase1") is False
    assert auth_service.is_valid_password("NOLOWERCASE1") is False
    assert auth_service.is_valid_password("NoNumbers") is False

def test_register_user(auth_service):
    auth_service.register_user("testuser@example.com", "SecureP@ss123")
    user = auth_service.auth_repository.get_user_by_email("testuser@example.com")
    assert user is not None
    assert user.email == "testuser@example.com"
    assert user.password_hash == auth_service.hash_password("SecureP@ss123")