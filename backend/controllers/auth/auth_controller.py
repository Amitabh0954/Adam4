from flask import Blueprint, request, jsonify
from backend.services.auth.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    auth_service = AuthService()

    if auth_service.is_email_taken(email):
        return jsonify({"error": "Email is already registered"}), 400

    if not auth_service.is_valid_password(password):
        return jsonify({"error": "Password does not meet security criteria"}), 400

    auth_service.register_user(email, password)
    return jsonify({"message": "User registered successfully"}), 201