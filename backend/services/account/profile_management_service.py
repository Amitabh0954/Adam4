```python  
"""
Profile Management Service
"""

from typing import Optional
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from backend.repositories.account.user_repository import UserRepository
from backend.models.account.user import User

class ProfileUpdateRequest(BaseModel):
    email: Optional[EmailStr]
    name: Optional[str]

class ProfileManagementService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def update_profile(self, user_id: int, request: ProfileUpdateRequest) -> User:
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        
        if request.email and request.email != user.email:
            if self.user_repository.get_user_by_email(request.email):
                raise ValueError("Email already registered")
            user.email = request.email
        
        if request.name:
            user.name = request.name
        
        self.user_repository.update_user(user)
        return user
```