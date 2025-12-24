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
    
    def get_product_by_id(self, product_id: int) -> Product:
        return self.db.query(Product).filter(Product.id == product_id).first()
    
    def update_product(self, product: Product) -> Product:
        self.db.commit()
        self.db.refresh(product)
        return product

    def delete_product(self, product: Product):
        self.db.delete(product)
        self.db.commit()
```