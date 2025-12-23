from backend.models.cart import Cart
from backend.repositories.cart.cart_repository import CartRepository

class CartService:
    def __init__(self):
        self.cart_repository = CartRepository()

    def get_cart(self, user_id: str) -> Cart:
        return self.cart_repository.get_cart(user_id) or Cart(user_id=user_id, items={})

    def add_product_to_cart(self, user_id: str, product_id: str, quantity: int) -> None:
        cart = self.get_cart(user_id)
        if product_id in cart.items:
            cart.items[product_id] += quantity
        else:
            cart.items[product_id] = quantity
        self.cart_repository.save_cart(cart)

    def remove_product_from_cart(self, user_id: str, product_id: str) -> None:
        cart = self.get_cart(user_id)
        if product_id in cart.items:
            del cart.items[product_id]
        self.cart_repository.save_cart(cart)