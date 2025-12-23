from typing import Optional
from backend.models.product import Product

class ProductRepository:
    def __init__(self):
        self.products = []

    def add_product(self, product: Product) -> None:
        self.products.append(product)

    def get_product_by_name(self, name: str) -> Optional[Product]:
        for product in self.products:
            if product.name == name:
                return product
        return None