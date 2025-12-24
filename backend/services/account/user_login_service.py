```python  
"""
User Login Service
"""

from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from backend.repositories.account.user_repository import UserRepository
from backend.models.account.user import User
from backend.config.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class TokenData:
    def __init__(self, user_id: int, expiration: datetime):
        self.user_id = user_id
        self.expiration = expiration

class UserLoginRequest:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

class UserLoginService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    def get_user(self, email: str) -> User:
        user = self.user_repository.get_user_by_email(email)
        if not user:
            raise ValueError("Invalid email or password")
        return user

    def authenticate_user(self, request: UserLoginRequest) -> User:
        user = self.get_user(request.email)
        if not self.verify_password(request.password, user.hashed_password):
            raise ValueError("Invalid email or password")
        return user

    def create_access_token(self, user_id: int):
        expiration = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        token_data = {"sub": str(user_id), "exp": expiration}
        token = jwt.encode(token_data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return token, expiration
```