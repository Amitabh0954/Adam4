from backend.models.product import Product
from backend.repositories.products.product_repository import ProductRepository

class ProductService:
    def __init__(self):
        self.product_repository = ProductRepository()

    def is_name_taken(self, name: str) -> bool:
        return self.product_repository.get_product_by_name(name) is not None

    def is_valid_price(self, price: float) -> bool:
        return price > 0

    def is_valid_description(self, description: str) -> bool:
        return bool(description.strip())

    def add_new_product(self, name: str, price: float, description: str, category: str) -> None:
        product = Product(name=name, price=price, description=description, category=category)
        self.product_repository.add_product(product)