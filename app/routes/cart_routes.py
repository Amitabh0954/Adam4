from flask import Blueprint, request, jsonify
from app.services.cart_service import CartService

cart_bp = Blueprint('cart', __name__, url_prefix='/cart')
cart_service = CartService()

@cart_bp.route('/save', methods=['POST'])
def save_cart() -> jsonify:
    data = request.json
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    try:
        cart_service.save_cart(user_id)
        return jsonify({'message': 'Cart saved successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@cart_bp.route('/retrieve', methods=['GET'])
def retrieve_cart() -> jsonify:
    user_id = request.args.get('user_id')

    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    try:
        cart = cart_service.retrieve_cart(user_id)
        return jsonify({'cart': cart}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
