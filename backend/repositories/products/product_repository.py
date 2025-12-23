from typing import Optional
from backend.models.product import Product

class ProductRepository:
    def __init__(self):
        self.products = []

    def add_product(self, product: Product) -> None:
        self.products.append(product)

    def update_product(self, updated_product: Product) -> None:
        for i, product in enumerate(self.products):
            if product.name == updated_product.name:
                self.products[i] = updated_product
                break

    def get_product_by_name(self, name: str) -> Optional[Product]:
        for product in self.products:
            if product.name == name:
                return product
        return None

    def delete_product(self, name: str) -> None:
        self.products = [product for product in self.products if product.name != name]