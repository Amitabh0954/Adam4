from typing import List, Optional, Tuple
from backend.models.product import Product
from backend.models.category import Category

class ProductRepository:
    def __init__(self):
        self.products = []
        self.categories = []

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

    def search_products(self, query: str, page: int, per_page: int) -> Tuple[List[Product], int]:
        matching_products = [product for product in self.products if query.lower() in product.name.lower() or query.lower() in product.category.lower()]
        total = len(matching_products)
        start = (page - 1) * per_page
        end = start + per_page
        return matching_products[start:end], total

    def add_category(self, category: Category) -> None:
        self.categories.append(category)

    def get_category_by_name(self, name: str) -> Optional[Category]:
        for category in self.categories:
            if category.name == name:
                return category
        return None

    def get_all_categories(self) -> List[Category]:
        return self.categories