```python  
"""
Category Management Controller
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.config.database import get_db
from backend.services.catalog.category_management_service import CategoryManagementService, CategoryCreateRequest
from backend.repositories.catalog.category_repository import CategoryRepository

router = APIRouter()

@router.post("/categories", response_model=dict)
def create_category(request: CategoryCreateRequest, db: Session = Depends(get_db)):
    category_repository = CategoryRepository(db)
    category_management_service = CategoryManagementService(category_repository)
    
    try:
        category = category_management_service.create_category(request)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return {"message": "Category created successfully", "category": {"id": category.id, "name": category.name, "parent_id": category.parent_id}}

@router.get("/categories", response_model=dict)
def list_categories(db: Session = Depends(get_db)):
    category_repository = CategoryRepository(db)
    category_management_service = CategoryManagementService(category_repository)
    
    categories = category_management_service.get_all_categories()
    
    return {"categories": [{"id": category.id, "name": category.name, "parent_id": category.parent_id} for category in categories]}
```