from typing import Optional, List
from backend.models.product import Product

class ProductRepository:
    def __init__(self):
        self.products = []

    def get_product_by_name(self, name: str) -> Optional[Product]:
        for product in self.products:
            if product.name == name:
                return product
        return None

    def add_product(self, product: Product) -> None:
        self.products.append(product)

    def get_all_products(self) -> List[Product]:
        return self.products

    def update_product(self, name: str, price: Optional[float], description: Optional[str]) -> Optional[Product]:
        product = self.get_product_by_name(name)
        if product is not None:
            if price is not None:
                product.price = price
            if description is not None:
                product.description = description
        return product

    def delete_product(self, name: str) -> bool:
        product = self.get_product_by_name(name)
        if product:
            self.products.remove(product)
            return True
        return False