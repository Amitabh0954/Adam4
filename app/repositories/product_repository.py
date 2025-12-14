from app.models.product import Product
from app.repositories.database import db

class ProductRepository:
    def get_product_by_id(self, product_id: int) -> Product:
        return Product.query.filter_by(id=product_id, is_deleted=False).first()

    def delete(self, product: Product) -> None:
        product.is_deleted = True
        db.session.commit()