import pytest
from backend.services.cart.cart_service import CartService

@pytest.fixture
def cart_service() -> CartService:
    return CartService()

def test_add_product_to_cart(cart_service):
    cart_id = cart_service.generate_guest_cart_id()
    cart_service.add_product_to_cart(cart_id, "Test Product", 2, persist=False)
    cart = cart_service.get_guest_cart(cart_id)
    assert cart["items"]["Test Product"] == 2

def test_get_user_cart(cart_service):
    cart_id = "user_123"
    cart_service.add_product_to_cart(cart_id, "Test Product", 2, persist=True)
    cart = cart_service.get_user_cart(cart_id)
    assert cart["items"]["Test Product"] == 2

def test_remove_product_from_cart(cart_service):
    cart_id = cart_service.generate_guest_cart_id()
    cart_service.add_product_to_cart(cart_id, "Test Product", 2, persist=False)
    cart_service.remove_product_from_cart(cart_id, "Test Product", persist=False)
    cart = cart_service.get_guest_cart(cart_id)
    assert "Test Product" not in cart["items"]

def test_calculate_total(cart_service):
    cart_id = cart_service.generate_guest_cart_id()
    cart_service.add_product_to_cart(cart_id, "Test Product", 2, persist=False)
    cart = cart_service.get_guest_cart(cart_id)
    total_price = cart_service.calculate_total(cart)
    assert total_price == 21.98