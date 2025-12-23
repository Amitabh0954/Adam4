from flask import Blueprint, request, jsonify, session
from backend.services.cart.cart_service import CartService
from backend.services.auth.auth_service import AuthService

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/add', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity')

    if not product_id or not quantity:
        return jsonify({"error": "Product ID and quantity are required"}), 400

    auth_service = AuthService()
    cart_service = CartService()

    if auth_service.is_logged_in():
        user_id = auth_service.get_current_user_id()
        cart_service.add_product_to_cart(user_id, product_id, quantity)
    else:
        session_cart = session.get('cart', {})
        session_cart[product_id] = session_cart.get(product_id, 0) + quantity
        session['cart'] = session_cart

    return jsonify({"message": "Product added to cart successfully"}), 200

@cart_bp.route('/view', methods=['GET'])
def view_cart():
    auth_service = AuthService()
    cart_service = CartService()

    if auth_service.is_logged_in():
        user_id = auth_service.get_current_user_id()
        cart = cart_service.get_cart(user_id)
    else:
        cart = session.get('cart', {})

    return jsonify(cart), 200

@cart_bp.route('/remove', methods=['POST'])
def remove_from_cart():
    data = request.get_json()
    product_id = data.get('product_id')

    if not product_id:
        return jsonify({"error": "Product ID is required"}), 400

    auth_service = AuthService()
    cart_service = CartService()

    if auth_service.is_logged_in():
        user_id = auth_service.get_current_user_id()
        cart_service.remove_product_from_cart(user_id, product_id)
    else:
        session_cart = session.get('cart', {})
        if product_id in session_cart:
            del session_cart[product_id]
            session['cart'] = session_cart

    return jsonify({"message": "Product removed from cart successfully"}), 200