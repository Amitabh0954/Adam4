```python  
"""
Product Delete Controller
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.config.database import get_db
from backend.services.catalog.product_delete_service import ProductDeleteService
from backend.repositories.catalog.product_repository import ProductRepository

router = APIRouter()

@router.delete("/products/{product_id}", response_model=dict)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product_repository = ProductRepository(db)
    product_delete_service = ProductDeleteService(product_repository)

    try:
        product = product_delete_service.delete_product(product_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return {"message": "Product deleted successfully", "product_id": product.id}
```