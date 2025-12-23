from backend.models.cart import Cart
from backend.repositories.cart_repository import CartRepository
from backend.services.products.product_service import ProductService
from uuid import uuid4

class CartService:
    def __init__(self):
        self.cart_repository = CartRepository()

    def generate_guest_cart_id(self) -> str:
        return str(uuid4())

    def add_product_to_cart(self, cart_id: str, product_id: str, quantity: int, persist: bool):
        cart = self.cart_repository.get_cart_by_id(cart_id) or Cart()
        cart.add_item(product_id, quantity)
        if persist:
            self.cart_repository.save_cart(cart_id, cart)

    def get_user_cart(self, user_id: str):
        return self.cart_repository.get_cart_by_id(user_id).to_dict() if self.cart_repository.get_cart_by_id(user_id) else {}

    def get_guest_cart(self, cart_id: str):
        return self.cart_repository.get_cart_by_id(cart_id).to_dict() if self.cart_repository.get_cart_by_id(cart_id) else {}

    def remove_product_from_cart(self, cart_id: str, product_id: str, persist: bool):
        cart = self.cart_repository.get_cart_by_id(cart_id)
        if cart:
            cart.remove_item(product_id)
            if persist:
                self.cart_repository.save_cart(cart_id, cart)
    
    def update_product_quantity(self, cart_id: str, product_id: str, quantity: int, persist: bool):
        cart = self.cart_repository.get_cart_by_id(cart_id)
        if cart:
            cart.update_quantity(product_id, quantity)
            if persist:
                self.cart_repository.save_cart(cart_id, cart)

    def calculate_total(self, cart: dict) -> float:
        total_price = 0.0
        product_service = ProductService()
        for product_id, quantity in cart.get('items', {}).items():
            product = product_service.get_product_by_id(product_id)
            if product:
                total_price += product.price * quantity
        return total_price