from flask import Blueprint, request, jsonify
from app.services.product_service import ProductService

product_bp = Blueprint('product', __name__, url_prefix='/product')
product_service = ProductService()


@product_bp.route('/delete', methods=['POST'])
def delete_product():
    """Endpoint for deleting a product."""
    data = request.json
    admin_token = data.get('admin_token')
    product_id = data.get('product_id')
    if not admin_token or not product_service.validate_admin(admin_token):
        return jsonify({'error': 'Unauthorized access'}), 403
    if not product_id:
        return jsonify({'error': 'Product ID is required'}), 400

    product_service.delete_product(product_id)
    return jsonify({'message': 'Product deleted successfully'}), 200