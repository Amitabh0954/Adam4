```python  
"""
Product Delete Service
"""

from backend.repositories.catalog.product_repository import ProductRepository
from backend.models.catalog.product import Product

class ProductDeleteService:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def delete_product(self, product_id: int) -> Product:
        product = self.product_repository.get_product_by_id(product_id)
        if not product:
            raise ValueError("Product not found")

        self.product_repository.delete_product(product)
        return product
```