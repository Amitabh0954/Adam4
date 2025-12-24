```python  
"""
Product Repository for Database Interactions
"""

from sqlalchemy.orm import Session
from backend.models.catalog.product import Product

class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_product(self, product: Product) -> Product:
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def get_product_by_name(self, name: str) -> Product:
        return self.db.query(Product).filter(Product.name == name).first()
```