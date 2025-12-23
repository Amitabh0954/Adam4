from typing import Optional
from backend.models.user import User

class AuthRepository:
    def __init__(self):
        self.users = {}

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.users.get(email)

    def save_user(self, user: User) -> None:
        self.users[user.email] = user

    def increment_failed_attempt(self, email: str) -> None:
        user = self.get_user_by_email(email)
        if user:
            user.failed_attempts += 1
            if user.failed_attempts >= 5:  # Example: lock account after 5 failed attempts
                user.account_locked = True
            self.save_user(user)

    def reset_failed_attempts(self, email: str) -> None:
        user = self.get_user_by_email(email)
        if user:
            user.failed_attempts = 0
            user.account_locked = False
            self.save_user(user)