from flask import Flask
from app.routes.product import product_bp

def init_routes(app: Flask) -> None:
    """Register all routes with the Flask app."""
    app.register_blueprint(product_bp)
