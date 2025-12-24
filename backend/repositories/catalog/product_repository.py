```python  
"""
Product Repository for Database Interactions
"""

from sqlalchemy.orm import Session
from sqlalchemy import or_
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
    
    def search_products(self, query: str, page: int, per_page: int) -> List[Product]:
        return self.db.query(Product).filter(
            or_(
                Product.name.ilike(f"%{query}%"),
                Product.description.ilike(f"%{query}%")
            )
        ).offset((page - 1) * per_page).limit(per_page).all()
```