import hashlib
import re
import jwt
import datetime
from backend.models.user import User
from backend.repositories.auth_repository import AuthRepository

class AuthService:
    def __init__(self):
        self.auth_repository = AuthRepository()
        self.jwt_secret = "your_secret_key"

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

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return self.hash_password(password) == hashed_password

    def register_user(self, email: str, password: str) -> None:
        password_hash = self.hash_password(password)
        user = User(email=email, password_hash=password_hash)
        self.auth_repository.save_user(user)

    def verify_user(self, email: str, password: str) -> bool:
        user = self.auth_repository.get_user_by_email(email)
        if not user:
            return False
        return self.verify_password(password, user.password_hash)

    def increment_failed_attempt(self, email: str) -> None:
        self.auth_repository.increment_failed_attempt(email)

    def reset_failed_attempts(self, email: str) -> None:
        self.auth_repository.reset_failed_attempts(email)

    def is_account_locked(self, email: str) -> bool:
        user = self.auth_repository.get_user_by_email(email)
        return user.account_locked if user else False

    def get_current_user_id(self) -> str:
        # Placeholder for the actual implementation to get current user ID
        return "user_id"

    def create_password_reset_token(self, email: str) -> str:
        expiry = datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        token = jwt.encode({'email': email, 'exp': expiry}, self.jwt_secret, algorithm='HS256')
        self.auth_repository.save_reset_token(email, token, expiry.isoformat())
        return token

    def validate_password_reset_token(self, token: str) -> bool:
        try:
            jwt.decode(token, self.jwt_secret, algorithms=['HS256'])
            user = self.auth_repository.get_user_by_reset_token(token)
            if not user or datetime.datetime.fromisoformat(user.reset_token_expiry) < datetime.datetime.utcnow():
                return False
            return True
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return False

    def send_password_reset_email(self, email: str, token: str) -> None:
        # Placeholder for email sending logic
        pass

    def update_password(self, token: str, new_password: str) -> None:
        user = self.auth_repository.get_user_by_reset_token(token)
        if user and self.validate_password_reset_token(token):
            user.password_hash = self.hash_password(new_password)
            self.auth_repository.save_user(user)
            self.auth_repository.clear_reset_token(user.email)