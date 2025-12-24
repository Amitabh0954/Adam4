```python  
"""
User Login Controller
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.config.database import get_db
from backend.services.account.user_login_service import UserLoginService, UserLoginRequest
from backend.repositories.account.user_repository import UserRepository

router = APIRouter()

@router.post("/login", response_model=dict)
def login(request: UserLoginRequest, db: Session = Depends(get_db)):
    user_repository = UserRepository(db)
    user_login_service = UserLoginService(user_repository)
    
    try:
        user = user_login_service.authenticate_user(request)
        access_token, expiration = user_login_service.create_access_token(user.id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return {"access_token": access_token, "token_type": "bearer", "expires": expiration}
```