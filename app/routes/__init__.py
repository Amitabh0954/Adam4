from flask import Flask
from app.routes.profile import profile_bp


def init_routes(app: Flask) -> None:
    """Register all routes with the Flask app."""
    app.register_blueprint(profile_bp)
