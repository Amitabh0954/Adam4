from typing import Optional
from backend.models.cart import Cart

class CartRepository:
    def __init__(self):
        self.carts = {}

    def get_cart_by_id(self, cart_id: str) -> Optional[Cart]:
        return self.carts.get(cart_id)

    def save_cart(self, cart_id: str, cart: Cart) -> None:
        self.carts[cart_id] = cart

    def delete_cart(self, cart_id: str) -> None:
        if cart_id in self.carts:
            del self.carts[cart_id]