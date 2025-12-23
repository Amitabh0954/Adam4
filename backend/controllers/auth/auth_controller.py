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
    session['user_id'] = auth_service.get_current_user_id(email)
    return jsonify({"message": "Logged in successfully"}), 200

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"}), 200

@auth_bp.route('/request_password_reset', methods=['POST'])
def request_password_reset():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({"error": "Email is required"}), 400

    auth_service = AuthService()
    if not auth_service.is_email_taken(email):
        return jsonify({"error": "Email not found"}), 404

    reset_token = auth_service.create_password_reset_token(email)
    auth_service.send_password_reset_email(email, reset_token)

    return jsonify({"message": "Password reset email sent"}), 200

@auth_bp.route('/reset_password', methods=['POST'])
def reset_password():
    data = request.get_json()
    token = data.get('token')
    new_password = data.get('new_password')

    if not token or not new_password:
        return jsonify({"error": "Token and new password are required"}), 400

    auth_service = AuthService()

    if not auth_service.validate_password_reset_token(token):
        return jsonify({"error": "Invalid or expired token"}), 400

    if not auth_service.is_valid_password(new_password):
        return jsonify({"error": "Password does not meet security criteria"}), 400

    auth_service.update_password(token, new_password)
    return jsonify({"message": "Password reset successfully"}), 200

@auth_bp.route('/profile', methods=['GET', 'PUT'])
def profile():
    auth_service = AuthService()
    user_id = session.get('user_id')

    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    if request.method == 'GET':
        user_profile = auth_service.get_user_profile(user_id)
        if not user_profile:
            return jsonify({"error": "User profile not found"}), 404
        return jsonify(user_profile), 200

    if request.method == 'PUT':
        data = request.get_json()
        updated_profile = auth_service.update_user_profile(user_id, data)
        return jsonify(updated_profile), 200