from backend.models.product import Product
from backend.repositories.product_repository import ProductRepository

class ProductService:
    def __init__(self):
        self.product_repository = ProductRepository()

    def is_product_name_taken(self, name: str) -> bool:
        return self.product_repository.get_product_by_name(name) is not None

    def add_product(self, name: str, price: float, description: str) -> Product:
        product = Product(name=name, price=price, description=description)
        self.product_repository.add_product(product)
        return product

    def get_all_products(self) -> list:
        return self.product_repository.get_all_products()

    def update_product(self, name: str, price: Optional[float], description: Optional[str]) -> Optional[Product]:
        return self.product_repository.update_product(name, price, description)