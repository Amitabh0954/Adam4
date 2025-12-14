"""
Application entry point.
"""

import logging
from flask import Flask
from app.routes.user_routes import user_blueprint
from app.services.user_service import UserService
from app.config.config import Config

class App:
    def __init__(self) -> None:
        self.app = Flask(__name__)
        self.configure_app()
        self.register_blueprints()
        self.init_services()

    def configure_app(self) -> None:
        self.app.config.from_object(Config)
        logging.basicConfig(level=logging.DEBUG)

    def register_blueprints(self) -> None:
        self.app.register_blueprint(user_blueprint)

    def init_services(self) -> None:
        self.user_service = UserService()

    def run(self) -> None:
        self.app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    app_instance = App()
    app_instance.run()
