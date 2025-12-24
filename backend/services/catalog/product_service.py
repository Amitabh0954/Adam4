```python  
"""
Product Management Service
"""

from pydantic import BaseModel, Field, validator
from backend.repositories.catalog.product_repository import ProductRepository
from backend.models.catalog.product import Product

class ProductCreateRequest(BaseModel):
    name: str
    description: str
    price: float
    category_id: int

    @validator('price')
    def price_must_be_positive(cls, value):
        if value <= 0:
            raise ValueError('Price must be a positive number')
        return value

class ProductService:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def add_new_product(self, request: ProductCreateRequest) -> Product:
        existing_product = self.product_repository.get_product_by_name(request.name)
        if existing_product:
            raise ValueError("Product name already exists")

        product = Product(
            name=request.name,
            description=request.description,
            price=request.price,
            category_id=request.category_id
        )
        
        return self.product_repository.create_product(product)
```