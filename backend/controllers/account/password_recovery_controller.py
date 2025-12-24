```python  
"""
Password Recovery Controller
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.config.database import get_db
from backend.services.account.password_recovery_service import PasswordRecoveryService
from backend.repositories.account.user_repository import UserRepository
from pydantic import BaseModel

class PasswordResetRequest(BaseModel):
    email: str

class PasswordResetConfirmRequest(BaseModel):
    token: str
    new_password: str

router = APIRouter()

@router.post("/password-reset", response_model=str)
def password_reset(request: PasswordResetRequest, db: Session = Depends(get_db)):
    user_repository = UserRepository(db)
    user = user_repository.get_user_by_email(request.email)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email not found")

    password_recovery_service = PasswordRecoveryService(user_repository)
    reset_token = password_recovery_service.create_reset_token(user.id)
    # Here you would typically send the reset_token to the user's email
    return f"Password reset link sent to {request.email}, token: {reset_token}"

@router.post("/password-reset-confirm", response_model=str)
def password_reset_confirm(request: PasswordResetConfirmRequest, db: Session = Depends(get_db)):
    user_repository = UserRepository(db)
    password_recovery_service = PasswordRecoveryService(user_repository)
    
    try:
        password_recovery_service.reset_password(request.token, request.new_password)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return "Password reset successfully"
```