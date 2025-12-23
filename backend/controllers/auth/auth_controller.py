from flask import Blueprint, request, jsonify, session
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

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    auth_service = AuthService()

    if auth_service.is_account_locked(email):
        return jsonify({"error": "Account is locked due to too many failed login attempts"}), 403

    if not auth_service.verify_user(email, password):
        auth_service.increment_failed_attempt(email)
        return jsonify({"error": "Invalid email or password"}), 401

    auth_service.reset_failed_attempts(email)
    session['user_id'] = auth_service.get_current_user_id()
    return jsonify({"message": "Logged in successfully"}), 200

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"}), 200