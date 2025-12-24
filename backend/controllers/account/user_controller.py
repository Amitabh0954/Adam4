```python  
"""
User Registration Controller
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.config.database import get_db
from backend.services.account.user_service import UserService, UserCreateRequest
from backend.repositories.account.user_repository import UserRepository

router = APIRouter()

@router.post("/register", response_model=str)
def register(request: UserCreateRequest, db: Session = Depends(get_db)):
    user_repository = UserRepository(db)
    user_service = UserService(user_repository)
    
    try:
        user_service.create_user(request)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return "User registered successfully"
```