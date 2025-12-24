```python  
"""
Product Management Controller
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.config.database import get_db
from backend.services.catalog.product_service import ProductService, ProductCreateRequest
from backend.repositories.catalog.product_repository import ProductRepository

router = APIRouter()

@router.post("/products", response_model=dict)
def add_product(request: ProductCreateRequest, db: Session = Depends(get_db)):
    product_repository = ProductRepository(db)
    product_service = ProductService(product_repository)
    
    try:
        product = product_service.add_new_product(request)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return {"message": "Product added successfully", "product": {"name": product.name, "description": product.description, "price": product.price, "category_id": product.category_id}}
```