```python  
"""
Password Recovery Service
"""

from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from backend.repositories.account.user_repository import UserRepository
from backend.models.account.user import User
from backend.config.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class PasswordRecoveryService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_reset_token(self, user_id: int):
        expiration = datetime.utcnow() + timedelta(hours=24)
        token_data = {"sub": str(user_id), "exp": expiration}
        token = jwt.encode(token_data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return token

    def verify_reset_token(self, token: str):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            user_id: int = int(payload.get("sub"))
            return user_id
        except JWTError:
            raise ValueError("Invalid or expired reset token")

    def reset_password(self, token: str, new_password: str):
        user_id = self.verify_reset_token(token)
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        hashed_password = pwd_context.hash(new_password)
        user.hashed_password = hashed_password
        self.user_repository.update_user(user)
        return user
```