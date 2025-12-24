```python  
"""
Product Search Controller
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.config.database import get_db
from backend.services.catalog.product_search_service import ProductSearchService
from backend.repositories.catalog.product_repository import ProductRepository

router = APIRouter()

@router.get("/products/search", response_model=dict)
def search_products(query: str, page: int = 1, per_page: int = 10, db: Session = Depends(get_db)):
    product_repository = ProductRepository(db)
    product_search_service = ProductSearchService(product_repository)
    
    products = product_search_service.search_products(query, page, per_page)
    
    return {"products": [{"name": product.name, "description": product.description, "price": product.price, "category_id": product.category_id} for product in products]}
```