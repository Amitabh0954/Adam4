from flask import Blueprint, request, jsonify
from backend.services.products.product_service import ProductService
from backend.services.products.category_service import CategoryService

product_bp = Blueprint('product', __name__)
category_bp = Blueprint('category', __name__)

@product_bp.route('/add', methods=['POST'])
def add_product():
    data = request.get_json()
    name = data.get('name')
    price = data.get('price')
    description = data.get('description')
    category_names = data.get('categories', [])

    if not name or not description or price is None:
        return jsonify({"error": "Name, description, and price are required"}), 400

    if price <= 0:
        return jsonify({"error": "Price must be a positive number"}), 400

    if not category_names:
        return jsonify({"error": "At least one category is required"}), 400

    product_service = ProductService()

    if product_service.is_product_name_taken(name):
        return jsonify({"error": "Product name is already taken"}), 400

    product = product_service.add_product(name, price, description, category_names)
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
    category_names = data.get('categories')

    if price is not None and not isinstance(price, (int, float)):
        return jsonify({"error": "Price must be a numeric value"}), 400

    if description == "":
        return jsonify({"error": "Description cannot be empty"}), 400

    product_service = ProductService()
    product = product_service.update_product(name, price, description, category_names)

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

@product_bp.route('/search', methods=['GET'])
def search_products():
    query = request.args.get('query')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    product_service = ProductService()
    search_results = product_service.search_products(query, page, per_page)
    return jsonify(search_results), 200

@category_bp.route('/add', methods=['POST'])
def add_category():
    data = request.get_json()
    name = data.get('name')
    parent_name = data.get('parent')

    if not name:
        return jsonify({"error": "Category name is required"}), 400

    category_service = CategoryService()
    category_service.add_category(name, parent_name)
    return jsonify({"message": "Category added successfully"}), 201

@category_bp.route('/list', methods=['GET'])
def list_categories():
    category_service = CategoryService()
    categories = category_service.get_all_categories()
    return jsonify([category.to_dict() for category in categories]), 200