from flask import Blueprint, request, jsonify
from app.services.category_service import CategoryService

category_bp = Blueprint('category', __name__, url_prefix='/category')
category_service = CategoryService()

@category_bp.route('/add', methods=['POST'])
def add_category():
    data = request.json
    category_service.add_category(data)
    return jsonify({'message': 'Category added successfully'}), 201

@category_bp.route('/update', methods=['POST'])
def update_category():
    data = request.json
    admin_token = data.get('admin_token')
    category_id = data.get('category_id')
    update_fields = {k: v for k, v in data.items() if k not in ['admin_token', 'category_id']}

    if not admin_token:
        return jsonify({'error': 'Admin token is required'}), 403

    if not category_service.validate_admin(admin_token):
        return jsonify({'error': 'Invalid admin token'}), 403

    category_service.update_category(category_id, update_fields)
    return jsonify({'message': 'Category details updated successfully'}), 200