"""
User routes.
"""

from flask import Blueprint, request, jsonify
from app.services.user_service import UserService

user_blueprint = Blueprint('user', __name__)
user_service = UserService()

@user_blueprint.route('/login', methods=['POST'])
def login() -> jsonify:
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Invalid input'}), 400
    user = user_service.login(username, password)
    if user:
        return jsonify({'message': 'Login successful', 'user': user}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401
