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

def test_verify_user(auth_service):
    auth_service.register_user("testuser@example.com", "SecureP@ss123")
    assert auth_service.verify_user("testuser@example.com", "SecureP@ss123") is True
    assert auth_service.verify_user("testuser@example.com", "WrongP@ss123") is False

def test_failed_attempts(auth_service):
    email = "testuser@example.com"
    auth_service.register_user(email, "SecureP@ss123")

    for _ in range(4):
        auth_service.increment_failed_attempt(email)
        assert auth_service.is_account_locked(email) is False

    auth_service.increment_failed_attempt(email)
    assert auth_service.is_account_locked(email) is True

    auth_service.reset_failed_attempts(email)
    assert auth_service.is_account_locked(email) is False
    assert auth_service.auth_repository.get_user_by_email(email).failed_attempts == 0