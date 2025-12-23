import hashlib
import re
from backend.models.user import User
from backend.repositories.auth_repository import AuthRepository

class AuthService:
    def __init__(self):
        self.auth_repository = AuthRepository()

    def is_email_taken(self, email: str) -> bool:
        return self.auth_repository.get_user_by_email(email) is not None

    def is_valid_password(self, password: str) -> bool:
        # Placeholder for actual password validation logic, should include checks for length, complexity, etc.
        if len(password) < 8:  # Example: password should be at least 8 characters long
            return False
        if not re.search(r'[A-Z]', password):  # Example: should contain at least one uppercase letter
            return False
        if not re.search(r'[a-z]', password):  # Example: should contain at least one lowercase letter
            return False
        if not re.search(r'[0-9]', password):  # Example: should contain at least one number
            return False
        return True

    def hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, email: str, password: str) -> None:
        password_hash = self.hash_password(password)
        user = User(email=email, password_hash=password_hash)
        self.auth_repository.save_user(user)