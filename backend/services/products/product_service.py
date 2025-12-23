from backend.models.product import Product
from backend.repositories.product_repository import ProductRepository
from backend.services.products.category_service import CategoryService

class ProductService:
    def __init__(self):
        self.product_repository = ProductRepository()
        self.category_service = CategoryService()

    def is_product_name_taken(self, name: str) -> bool:
        return self.product_repository.get_product_by_name(name) is not None

    def add_product(self, name: str, price: float, description: str, category_names: list) -> Product:
        for category_name in category_names:
            if not self.category_service.is_category_exist(category_name):
                raise ValueError(f"Category {category_name} does not exist")
        product = Product(name=name, price=price, description=description, categories=category_names)
        self.product_repository.add_product(product)
        return product

    def get_all_products(self) -> list:
        return self.product_repository.get_all_products()

    def update_product(self, name: str, price: Optional[float], description: Optional[str], category_names: list) -> Optional[Product]:
        if category_names is not None:
            for category_name in category_names:
                if not self.category_service.is_category_exist(category_name):
                    raise ValueError(f"Category {category_name} does not exist")
        return self.product_repository.update_product(name, price, description, category_names)

    def delete_product(self, name: str) -> bool:
        return self.product_repository.delete_product(name)

    def search_products(self, query: str, page: int, per_page: int) -> dict:
        return self.product_repository.search_products(query, page, per_page)