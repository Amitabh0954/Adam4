from app.models.user import User
from app.repositories.database import db

class UserRepository:
    def find_by_id(self, user_id: int) -> User:
        """Find user by ID."""
        return User.query.get(user_id)

    def save(self, user: User) -> None:
        """Save user instance."""
        user.save()