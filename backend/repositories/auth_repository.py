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

    def save_reset_token(self, email: str, token: str, expiry: str) -> None:
        user = self.get_user_by_email(email)
        if user:
            user.reset_token = token
            user.reset_token_expiry = expiry
            self.save_user(user)

    def get_user_by_reset_token(self, token: str) -> Optional[User]:
        for user in self.users.values():
            if user.reset_token == token:
                return user
        return None

    def clear_reset_token(self, email: str) -> None:
        user = self.get_user_by_email(email)
        if user:
            user.reset_token = None
            user.reset_token_expiry = None
            self.save_user(user)