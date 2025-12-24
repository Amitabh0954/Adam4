```python  
"""
Shopping Cart Model Definition
"""

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from backend.config.database import Base

class ShoppingCart(Base):
    __tablename__ = "shopping_carts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="shopping_cart")
    items = relationship("CartItem", cascade="all, delete-orphan", back_populates="cart")
```