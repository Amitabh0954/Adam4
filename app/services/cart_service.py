from app.repositories.cart_repository import CartRepository
from app.repositories.product_repository import ProductRepository

class CartService:
    def __init__(self):
        self.cart_repository = CartRepository()
        self.product_repository = ProductRepository()

    def add_to_cart(self, user_id: int, product_id: int, quantity: int) -> None:
        product = self.product_repository.get_product_by_id(product_id)
        if not product:
            raise ValueError('Product not found')
        self.cart_repository.add_product_to_cart(user_id, product_id, quantity)
