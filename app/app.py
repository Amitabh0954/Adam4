import os
from flask import Flask
from app.config import Config
from app.routes import register_blueprints
from app.repositories.database import db


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    register_blueprints(app)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
