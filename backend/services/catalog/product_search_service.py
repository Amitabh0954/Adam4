```python  
"""
Product Search Service
"""

from typing import List
from sqlalchemy.orm import Session
from backend.repositories.catalog.product_repository import ProductRepository
from backend.models.catalog.product import Product

class ProductSearchService:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def search_products(self, query: str, page: int = 1, per_page: int = 10) -> List[Product]:
        return self.product_repository.search_products(query, page, per_page)
```