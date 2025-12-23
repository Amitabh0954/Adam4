from flask import Blueprint, request, jsonify, session
from backend.services.cart.cart_service import CartService
from backend.services.products.product_service import ProductService

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/add', methods=['POST'])
def add_to_cart():
    product_id = request.get_json().get('product_id')
    quantity = request.get_json().get('quantity', 1)

    if quantity <= 0:
        return jsonify({"error": "Quantity must be a positive integer"}), 400

    product_service = ProductService()
    product = product_service.get_product_by_id(product_id)

    if not product:
        return jsonify({"error": "Product not found"}), 404

    cart_service = CartService()

    if 'user_id' in session:
        user_id = session['user_id']
        cart_service.add_product_to_cart(user_id, product_id, quantity, persist=True)
    else:
        cart_id = session.get('cart_id', None)
        if not cart_id:
            cart_id = cart_service.generate_guest_cart_id()
            session['cart_id'] = cart_id
        cart_service.add_product_to_cart(cart_id, product_id, quantity, persist=False)

    return jsonify({"message": "Product added to cart successfully"}), 200


@cart_bp.route('/view', methods=['GET'])
def view_cart():
    cart_service = CartService()

    if 'user_id' in session:
        user_id = session['user_id']
        cart = cart_service.get_user_cart(user_id)
    else:
        cart_id = session.get('cart_id', None)
        if not cart_id:
            return jsonify({"cart": []}), 200
        cart = cart_service.get_guest_cart(cart_id)

    total_price = cart_service.calculate_total(cart)
    return jsonify({"cart": cart, "total_price": total_price}), 200


@cart_bp.route('/remove', methods=['POST'])
def remove_from_cart():
    product_id = request.get_json().get('product_id')
    confirmation = request.get_json().get('confirm')

    if not confirmation:
        return jsonify({"error": "Confirmation required to remove product"}), 400

    cart_service = CartService()

    if 'user_id' in session:
        user_id = session['user_id']
        cart_service.remove_product_from_cart(user_id, product_id, persist=True)
    else:
        cart_id = session.get('cart_id', None)
        if not cart_id:
            return jsonify({"error": "No cart found"}), 404
        cart_service.remove_product_from_cart(cart_id, product_id, persist=False)

    return jsonify({"message": "Product removed from cart successfully"}), 200

@cart_bp.route('/update', methods=['POST'])
def update_cart():
    product_id = request.get_json().get('product_id')
    quantity = request.get_json().get('quantity')

    if quantity <= 0:
        return jsonify({"error": "Quantity must be a positive integer"}), 400

    cart_service = CartService()

    if 'user_id' in session:
        user_id = session['user_id']
        cart_service.update_product_quantity(user_id, product_id, quantity, persist=True)
    else:
        cart_id = session.get('cart_id', None)
        if not cart_id:
            return jsonify({"error": "No cart found"}), 404
        cart_service.update_product_quantity(cart_id, product_id, quantity, persist=False)

    total_price = cart_service.calculate_total(cart_service.get_user_cart(user_id) if 'user_id' in session else cart_service.get_guest_cart(cart_id))
    return jsonify({"message": "Cart updated successfully", "total_price": total_price}), 200