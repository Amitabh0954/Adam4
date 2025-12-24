```python  
"""
Product Update Service
"""

from pydantic import BaseModel, Field, validator
from typing import Optional
from backend.repositories.catalog.product_repository import ProductRepository
from backend.models.catalog.product import Product

class ProductUpdateRequest(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]

    @validator('price')
    def price_must_be_positive(cls, value):
        if value is not None and value <= 0:
            raise ValueError('Price must be a positive number')
        return value

class ProductUpdateService:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def update_product(self, product_id: int, request: ProductUpdateRequest) -> Product:
        product = self.product_repository.get_product_by_id(product_id)
        if not product:
            raise ValueError("Product not found")

        if request.name:
            if (existing_product := self.product_repository.get_product_by_name(request.name)) and existing_product.id != product_id:
                raise ValueError("Product name already exists")

            product.name = request.name

        if request.description:
            product.description = request.description

        if request.price:
            product.price = request.price
        
        self.product_repository.update_product(product)
        return product
```