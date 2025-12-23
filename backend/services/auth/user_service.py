import re
from backend.models.user import User
from backend.repositories.auth.user_repository import UserRepository

class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    def is_email_taken(self, email: str) -> bool:
        return self.user_repository.get_user_by_email(email) is not None

    def is_valid_password(self, password: str) -> bool:
        if len(password) < 8:
            return False
        if not re.search(r'[A-Z]', password):
            return False
        if not re.search(r'[a-z]', password):
            return False
        if not re.search(r'[0-9]', password):
            return False
        if not re.search(r'[@$!%*?&#]', password):
            return False
        return True

    def create_user(self, email: str, password: str) -> None:
        user = User(email=email, password=password)
        self.user_repository.add_user(user)