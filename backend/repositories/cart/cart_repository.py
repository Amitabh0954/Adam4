```python  
"""
Cart Repository for Database Interactions
"""

from sqlalchemy.orm import Session
from backend.models.cart.shopping_cart import ShoppingCart
from backend.models.cart.cart_item import CartItem
from typing import List

class CartRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_cart_by_user_id(self, user_id: int) -> ShoppingCart:
        return self.db.query(ShoppingCart).filter(ShoppingCart.user_id == user_id).first()

    def create_cart(self, user_id: int) -> ShoppingCart:
        cart = ShoppingCart(user_id=user_id)
        self.db.add(cart)
        self.db.commit()
        self.db.refresh(cart)
        return cart

    def add_product_to_cart(self, cart: ShoppingCart, product_id: int, quantity: int = 1) -> CartItem:
        cart_item = CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity)
        self.db.add(cart_item)
        self.db.commit()
        self.db.refresh(cart_item)
        return cart_item

    def remove_product_from_cart(self, cart: ShoppingCart, product_id: int):
        cart_item = self.db.query(CartItem).filter(CartItem.cart_id == cart.id, CartItem.product_id == product_id).first()
        if cart_item:
            self.db.delete(cart_item)
            self.db.commit()

    def get_cart_items(self, cart_id: int) -> List[CartItem]:
        return self.db.query(CartItem).filter(CartItem.cart_id == cart_id).all()
```