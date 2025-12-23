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

    if quantity <= 0:
        return jsonify({"error": "Quantity must be a positive integer"}), 400

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

    cart_total = cart_service.calculate_cart_total(cart.items)
    cart_data = {"items": cart.items, "total": cart_total}

    return jsonify(cart_data), 200

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

@cart_bp.route('/update_quantity', methods=['POST'])
def update_quantity():
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity')

    if not product_id or not quantity:
        return jsonify({"error": "Product ID and quantity are required"}), 400

    if quantity <= 0:
        return jsonify({"error": "Quantity must be a positive integer"}), 400

    auth_service = AuthService()
    cart_service = CartService()

    if auth_service.is_logged_in():
        user_id = auth_service.get_current_user_id()
        cart_service.update_product_quantity_in_cart(user_id, product_id, quantity)
    else:
        session_cart = session.get('cart', {})
        if product_id in session_cart:
            session_cart[product_id] = quantity
            session['cart'] = session_cart

    cart_total = cart_service.calculate_cart_total(session_cart) if not auth_service.is_logged_in() else cart_service.calculate_cart_total(cart_service.get_cart(user_id).items)

    return jsonify({"message": "Quantity updated successfully", "total": cart_total}), 200