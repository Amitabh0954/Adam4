from app.repositories.database import db
from app.models.product import Product

class ShoppingCart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    products = db.relationship('Product', secondary='cart_products', backref=db.backref('carts', lazy=True))

    def add_product(self, product: Product) -> None:
        self.products.append(product)

    def remove_product(self, product_id: int) -> None:
        product_to_remove = next((p for p in self.products if p.id == product_id), None)
        if product_to_remove:
            self.products.remove(product_to_remove)

    def calculate_total_price(self) -> float:
        return sum(product.price for product in self.products)

# Association table for many-to-many relationship
cart_products = db.Table('cart_products',
    db.Column('cart_id', db.Integer, db.ForeignKey('shopping_cart.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
)
