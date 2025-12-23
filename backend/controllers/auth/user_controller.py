from flask import Blueprint, request, jsonify
from backend.models.user import User
from backend.services.auth.user_service import UserService

user_bp = Blueprint('user', __name__)

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user_service = UserService()

    if user_service.is_email_taken(email):
        return jsonify({"error": "Email must be unique"}), 400

    if not user_service.is_valid_password(password):
        return jsonify({"error": "Password must meet security criteria"}), 400

    user_service.create_user(email, password)

    return jsonify({"message": "User registered successfully"}), 201

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user_service = UserService()

    if user_service.authenticate_user(email, password):
        return jsonify({"message": "Login successful"}), 200

    return jsonify({"error": "Invalid email or password"}), 401