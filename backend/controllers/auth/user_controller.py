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

@user_bp.route('/reset_password', methods=['POST'])
def reset_password():
    data = request.get_json()
    email = data.get('email')

    user_service = UserService()

    if not user_service.is_email_taken(email):
        return jsonify({"error": "Email not registered"}), 400

    reset_link = user_service.generate_reset_link(email)
    return jsonify({"message": f"Password reset link sent to {email}"}), 200

@user_bp.route('/profile', methods=['PUT'])
def update_profile():
    data = request.get_json()
    email = data.get('email')
    new_data = {
        "name": data.get('name'),
        "phone": data.get('phone')
    }

    user_service = UserService()

    if not user_service.is_email_taken(email):
        return jsonify({"error": "Email not registered"}), 400

    updated_user = user_service.update_user_profile(email, new_data)
    return jsonify({
        "message": "Profile updated successfully",
        "user": updated_user
    }), 200