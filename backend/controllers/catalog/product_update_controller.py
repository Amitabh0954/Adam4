```python  
"""
Product Update Controller
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.config.database import get_db
from backend.services.catalog.product_update_service import ProductUpdateService, ProductUpdateRequest
from backend.repositories.catalog.product_repository import ProductRepository

router = APIRouter()

@router.put("/products/{product_id}", response_model=dict)
def update_product(product_id: int, request: ProductUpdateRequest, db: Session = Depends(get_db)):
    product_repository = ProductRepository(db)
    product_update_service = ProductUpdateService(product_repository)

    try:
        product = product_update_service.update_product(product_id, request)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return {"message": "Product updated successfully", "product": {"name": product.name, "description": product.description, "price": product.price, "category_id": product.category_id}}
```