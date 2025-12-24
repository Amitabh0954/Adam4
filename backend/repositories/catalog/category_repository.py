```python  
"""
Category Repository for Database Interactions
"""

from sqlalchemy.orm import Session
from backend.models.catalog.category import Category
from typing import List

class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_category(self, category: Category) -> Category:
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category
    
    def get_category_by_id(self, category_id: int) -> Category:
        return self.db.query(Category).filter(Category.id == category_id).first()
    
    def get_all_categories(self) -> List<Category]:
        return self.db.query(Category).all()
```