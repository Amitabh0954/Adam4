```python  
"""
Cart Service to Handle Business Logic
"""

from backend.repositories.cart.cart_repository import CartRepository

class CartService:
    def __init__(self, cart_repository: CartRepository):
        self.cart_repository = cart_repository

    def add_product_to_cart(self, user_id: int, product_id: int, quantity: int = 1):
        cart = self.cart_repository.get_cart_by_user_id(user_id)
        if not cart:
            cart = self.cart_repository.create_cart(user_id)

        return self.cart_repository.add_product_to_cart(cart, product_id, quantity)

    def remove_product_from_cart(self, user_id: int, product_id: int):
        cart = self.cart_repository.get_cart_by_user_id(user_id)
        if not cart:
            raise ValueError("Cart not found")

        self.cart_repository.remove_product_from_cart(cart, product_id)

    def modify_product_quantity(self, user_id: int, product_id: int, quantity: int):
        cart = self.cart_repository.get_cart_by_user_id(user_id)
        if not cart:
            raise ValueError("Cart not found")
        
        if quantity <= 0:
            raise ValueError("Quantity must be a positive integer")

        self.cart_repository.modify_product_quantity(cart, product_id, quantity)

    def get_cart(self, user_id: int):
        cart = self.cart_repository.get_cart_by_user_id(user_id)
        if not cart:
            raise ValueError("Cart not found")

        return cart
```