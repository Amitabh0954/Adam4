from app.models.product import Product
from app.repositories.product_repository import ProductRepository
from werkzeug.security import check_password_hash

class ProductService:
    def __init__(self):
        self.product_repository = ProductRepository()

    def validate_admin(self, admin_token: str) -> bool:
        # Placeholder for admin validation logic
        # In production, validate the admin token against stored secrets
        return admin_token == 'valid_admin_token'

    def update_product(self, product_id: int, update_fields: dict) -> None:
        product = self.product_repository.get_product_by_id(product_id)
        if not product:
            raise ValueError('Product not found')

        if 'price' in update_fields and not isinstance(update_fields['price'], (int, float)):
            raise ValueError('Price must be numeric')

        for key, value in update_fields.items():
            if hasattr(product, key):
                setattr(product, key, value)

        self.product_repository.save_product(product)
