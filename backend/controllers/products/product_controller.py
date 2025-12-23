from flask import Blueprint, request, jsonify
from backend.services.products.product_service import ProductService

product_bp = Blueprint('product', __name__)

@product_bp.route('/add', methods=['POST'])
def add_product():
    data = request.get_json()
    name = data.get('name')
    price = data.get('price')
    description = data.get('description')

    if not name or not description or price is None:
        return jsonify({"error": "Name, description, and price are required"}), 400

    if price <= 0:
        return jsonify({"error": "Price must be a positive number"}), 400

    product_service = ProductService()

    if product_service.is_product_name_taken(name):
        return jsonify({"error": "Product name is already taken"}), 400

    product = product_service.add_product(name, price, description)
    return jsonify(product.to_dict()), 201

@product_bp.route('/list', methods=['GET'])
def list_products():
    product_service = ProductService()
    products = product_service.get_all_products()
    return jsonify([product.to_dict() for product in products]), 200

@product_bp.route('/update/<string:name>', methods=['PUT'])
def update_product(name):
    data = request.get_json()
    price = data.get('price')
    description = data.get('description')

    if price is not None and not isinstance(price, (int, float)):
        return jsonify({"error": "Price must be a numeric value"}), 400

    if description == "":
        return jsonify({"error": "Description cannot be empty"}), 400

    product_service = ProductService()
    product = product_service.update_product(name, price, description)

    if not product:
        return jsonify({"error": "Product not found"}), 404

    return jsonify(product.to_dict()), 200

@product_bp.route('/delete/<string:name>', methods=['DELETE'])
def delete_product(name):
    product_service = ProductService()
    confirmation = request.args.get('confirm')

    if confirmation != 'yes':
        return jsonify({"error": "Confirmation required to delete product"}), 400

    if product_service.delete_product(name):
        return jsonify({"message": "Product deleted successfully"}), 200

    return jsonify({"error": "Product not found"}), 404