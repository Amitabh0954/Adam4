from typing import Optional
from backend.models.user import User

class UserRepository:
    def __init__(self):
        self.users = []

    def add_user(self, user: User) -> None:
        self.users.append(user)
    
    def update_user(self, user: User) -> None:
        # simplistic update logic; in a real database, this would ensure the entry gets updated
        self.delete_user(user.email)
        self.add_user(user)

    def get_user_by_email(self, email: str) -> Optional[User]:
        for user in self.users:
            if user.email == email:
                return user
        return None
    
    def delete_user(self, email: str) -> None:
        self.users = [user for user in self.users if user.email != email]