from app.models.user import User
from app.repositories.user_repository import UserRepository

class ProfileService:
    def __init__(self):
        self.user_repository = UserRepository()

    def update_profile(self, data: dict) -> dict:
        """Update user profile and persist changes."""
        user_id = data.get('user_id')
        user = self.user_repository.find_by_id(user_id)
        if user:
            user.name = data.get('name', user.name)
            user.email = data.get('email', user.email)
            self.user_repository.save(user)
            return {'message': 'Profile updated successfully'}
        else:
            return {'error': 'User not found'}
