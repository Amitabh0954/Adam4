from flask import Blueprint, request, jsonify
from app.services.product_service import ProductService

product_bp = Blueprint('product', __name__, url_prefix='/product')
product_service = ProductService()

@product_bp.route('/add', methods=['POST'])
def add_product():
    data = request.json
    product_service.add_product(data)
    return jsonify({'message': 'Product added successfully'}), 201
