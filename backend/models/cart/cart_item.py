```python  
"""
Cart Item Model Definition
"""

from sqlalchemy import Column, Integer, ForeignKey
from backend.config.database import Base

class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey("shopping_carts.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    
    # Relationships
    cart = relationship("ShoppingCart", back_populates="items")
    product = relationship("Product")
```