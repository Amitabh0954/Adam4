from typing import Optional
from backend.models.user import User

class AuthRepository:
    def __init__(self):
        self.users = {}

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.users.get(email)

    def save_user(self, user: User) -> None:
        self.users[user.email] = user