from app.models.product import Product
from app.repositories.product_repository import ProductRepository

class ProductService:
    def __init__(self):
        self.product_repository = ProductRepository()

    def validate_admin(self, admin_token: str) -> bool:
        # Placeholder for admin validation logic
        return admin_token == "valid_admin_token"

    def delete_product(self, product_id: int) -> None:
        product = self.product_repository.get_product_by_id(product_id)
        if product:
            self.product_repository.delete(product)
        else:
            raise ValueError('Product not found')
