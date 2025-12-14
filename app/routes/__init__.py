# __init__.py
from flask import Flask
from app.routes.product_routes import product_bp
from app.routes.category_routes import category_bp


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(product_bp)
    app.register_blueprint(category_bp)
