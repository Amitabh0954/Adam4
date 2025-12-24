```python  
"""
Profile Management Controller
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.config.database import get_db
from backend.services.account.profile_management_service import ProfileManagementService, ProfileUpdateRequest
from backend.repositories.account.user_repository import UserRepository

router = APIRouter()

@router.put("/profile", response_model=dict)
def update_profile(user_id: int, request: ProfileUpdateRequest, db: Session = Depends(get_db)):
    user_repository = UserRepository(db)
    profile_management_service = ProfileManagementService(user_repository)
    
    try:
        user = profile_management_service.update_profile(user_id, request)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return {"message": "Profile updated successfully", "user": {"email": user.email, "name": user.name}}
```