from typing import Optional
from backend.models.cart import Cart

class CartRepository:
    def __init__(self):
        self.carts = {}

    def get_cart(self, user_id: str) -> Optional[Cart]:
        return self.carts.get(user_id)

    def save_cart(self, cart: Cart) -> None:
        self.carts[cart.user_id] = cart