from flask import Blueprint, request, jsonify
from backend.services.products.product_service import ProductService

category_bp = Blueprint('category', __name__)

@category_bp.route('/add_category', methods=['POST'])
def add_category():
    data = request.get_json()
    name = data.get('name')
    parent = data.get('parent')

    if not name:
        return jsonify({"error": "Category name is required"}), 400

    product_service = ProductService()
    product_service.add_category(name, parent)

    return jsonify({"message": "Category added successfully"}), 201

@category_bp.route('/categories', methods=['GET'])
def get_categories():
    product_service = ProductService()
    categories = product_service.get_all_categories()
    return jsonify(categories), 200