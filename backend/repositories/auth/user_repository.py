from typing import Optional
from backend.models.user import User

class UserRepository:
    def __init__(self):
        self.users = []

    def add_user(self, user: User) -> None:
        self.users.append(user)

    def get_user_by_email(self, email: str) -> Optional[User]:
        for user in self.users:
            if user.email == email:
                return user
        return None