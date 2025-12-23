from typing import List, Tuple
from backend.models.product import Product
from backend.models.category import Category
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

    def update_product_details(self, name: str, price: float, description: str, category: str) -> None:
        existing_product = self.product_repository.get_product_by_name(name)
        if existing_product:
            updated_product = Product(name=name, price=price, description=description, category=category)
            self.product_repository.update_product(updated_product)

    def delete_product(self, name: str) -> None:
        self.product_repository.delete_product(name)
    
    def search_products(self, query: str, page: int, per_page: int) -> Tuple[List[Product], int]:
        return self.product_repository.search_products(query, page, per_page)
    
    def add_category(self, name: str, parent: Optional[str] = None) -> None:
        category = Category(name=name, parent=parent)
        parent_category = self.product_repository.get_category_by_name(parent) if parent else None
        if parent_category:
            parent_category.children.append(name)
        self.product_repository.add_category(category)

    def get_all_categories(self) -> List[Category]:
        return self.product_repository.get_all_categories()