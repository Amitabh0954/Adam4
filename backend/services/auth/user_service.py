import re
from backend.models.user import User
from backend.repositories.auth.user_repository import UserRepository

class UserService:
    def __init__(self):
        self.user_repository = UserRepository()
        self.failed_logins = {}

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

    def authenticate_user(self, email: str, password: str) -> bool:
        user = self.user_repository.get_user_by_email(email)
        if user and user.password == password:
            self.failed_logins[email] = 0  # reset failed login attempts
            return True
        
        # record failed attempt
        self.failed_logins[email] = self.failed_logins.get(email, 0) + 1

        if self.failed_logins[email] > 3:
            # you can implement further actions like temporary lock on account
            return False
        return False