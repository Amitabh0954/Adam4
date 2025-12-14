from app.models.product import Product
from app.repositories.product_repository import ProductRepository

class ProductService:
    def __init__(self):
        self.repository = ProductRepository()

    def add_product(self, data: dict) -> None:
        product = Product(
            name=data['name'],
            price=data['price'],
            description=data['description'],
            category_id=data['category_id']
        )
        self.repository.add(product)

    def validate_admin(self, admin_token: str) -> bool:
        # Placeholder for admin validation logic
        return admin_token == 'valid_admin_token'

    def update_product(self, product_id: int, update_fields: dict) -> None:
        product = self.repository.get_product_by_id(product_id)
        if 'price' in update_fields and not isinstance(update_fields['price'], (int, float)):
            raise ValueError('Price must be numeric')
        for key, value in update_fields.items():
            if hasattr(product, key):
                setattr(product, key, value)
        self.repository.save(product)
