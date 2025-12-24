```python  
"""
User Management Service
"""

from pydantic import BaseModel, EmailStr, Field
from backend.repositories.account.user_repository import UserRepository
from backend.models.account.user import User
from passlib.context import CryptContext
from typing import Optional

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserCreateRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user(self, request: UserCreateRequest) -> User:
        existing_user = self.user_repository.get_user_by_email(request.email)
        if existing_user:
            raise ValueError("Email already registered")

        hashed_password = pwd_context.hash(request.password)
        user = User(email=request.email, hashed_password=hashed_password)
        return self.user_repository.create_user(user)
```