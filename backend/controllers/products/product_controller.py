from flask import Blueprint, request, jsonify
from backend.services.products.product_service import ProductService

product_bp = Blueprint('product', __name__)

@product_bp.route('/add', methods=['POST'])
def add_product():
    data = request.get_json()
    name = data.get('name')
    price = data.get('price')
    description = data.get('description')
    category = data.get('category')

    product_service = ProductService()

    if product_service.is_name_taken(name):
        return jsonify({"error": "Product name must be unique"}), 400

    if not product_service.is_valid_price(price):
        return jsonify({"error": "Product price must be a positive number"}), 400

    if not product_service.is_valid_description(description):
        return jsonify({"error": "Product description cannot be empty"}), 400

    product_service.add_new_product(name, price, description, category)

    return jsonify({"message": "Product added successfully"}), 201

@product_bp.route('/update', methods=['PUT'])
def update_product():
    data = request.get_json()
    name = data.get('name')
    price = data.get('price')
    description = data.get('description')
    category = data.get('category')

    product_service = ProductService()

    if not product_service.is_name_taken(name):
        return jsonify({"error": "Product not found"}), 404

    if not product_service.is_valid_price(price):
        return jsonify({"error": "Product price must be a positive number"}), 400

    if not description.strip():
        return jsonify({"error": "Product description cannot be empty"}), 400

    product_service.update_product_details(name, price, description, category)

    return jsonify({"message": "Product updated successfully"}), 200