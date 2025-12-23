from flask import Flask
from backend.controllers.auth.user_controller import user_bp

def create_app() -> Flask:
    app = Flask(__name__)

    # Register Blueprints
    app.register_blueprint(user_bp, url_prefix='/auth')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)