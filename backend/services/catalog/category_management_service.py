```python  
"""
Category Management Service
"""

from pydantic import BaseModel
from backend.repositories.catalog.category_repository import CategoryRepository
from backend.models.catalog.category import Category
from typing import List

class CategoryCreateRequest(BaseModel):
    name: str
    parent_id: int = None

class CategoryManagementService:
    def __init__(self, category_repository: CategoryRepository):
        self.category_repository = category_repository

    def create_category(self, request: CategoryCreateRequest) -> Category:
        if request.parent_id:
            parent_category = self.category_repository.get_category_by_id(request.parent_id)
            if not parent_category:
                raise ValueError("Parent category not found")
        
        category = Category(
            name=request.name,
            parent_id=request.parent_id
        )
        
        return self.category_repository.create_category(category)

    def get_all_categories(self) -> List[Category]:
        return self.category_repository.get_all_categories()
```