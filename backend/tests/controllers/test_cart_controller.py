import pytest
from flask import Flask, session
from backend.app import create_app

@pytest.fixture
def app() -> Flask:
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SECRET_KEY": "test_secret_key",
    })
    return app

@pytest.fixture
def client(app: Flask):
    return app.test_client()

def test_add_to_cart(client):
    client.post('/products/add', json={
        "name": "Test Product",
        "price": 10.99,
        "description": "A test product"
    })
    response = client.post('/cart/add', json={
        "product_id": "Test Product",
        "quantity": 2
    })
    assert response.status_code == 200
    assert response.get_json() == {"message": "Product added to cart successfully"}

def test_view_cart(client):
    client.post('/products/add', json={
        "name": "Test Product",
        "price": 10.99,
        "description": "A test product"
    })
    client.post('/cart/add', json={
        "product_id": "Test Product",
        "quantity": 2
    })
    response = client.get('/cart/view')
    assert response.status_code == 200
    cart = response.get_json()["cart"]
    assert "Test Product" in cart["items"]
    assert cart["items"]["Test Product"] == 2
    total_price = response.get_json()["total_price"]
    assert total_price == 21.98

def test_remove_from_cart(client):
    client.post('/products/add', json={
        "name": "Test Product",
        "price": 10.99,
        "description": "A test product"
    })
    client.post('/cart/add', json={
        "product_id": "Test Product",
        "quantity": 2
    })
    response = client.post('/cart/remove', json={"product_id": "Test Product", "confirm": True})
    assert response.status_code == 200
    assert response.get_json() == {"message": "Product removed from cart successfully"}
    response = client.get('/cart/view')
    assert response.status_code == 200
    cart = response.get_json()["cart"]
    assert "items" in cart
    assert "Test Product" not in cart["items"]

def test_remove_from_cart_without_confirmation(client):
    client.post('/products/add', json={
        "name": "Test Product",
        "price": 10.99,
        "description": "A test product"
    })
    client.post('/cart/add', json={
        "product_id": "Test Product",
        "quantity": 2
    })
    response = client.post('/cart/remove', json={"product_id": "Test Product"})
    assert response.status_code == 400
    assert response.get_json() == {"error": "Confirmation required to remove product"}

def test_update_cart(client):
    client.post('/products/add', json={
        "name": "Test Product",
        "price": 10.99,
        "description": "A test product"
    })
    client.post('/cart/add', json={
        "product_id": "Test Product",
        "quantity": 2
    })
    response = client.post('/cart/update', json={"product_id": "Test Product", "quantity": 5})
    assert response.status_code == 200
    assert response.get_json()["message"] == "Cart updated successfully"
    total_price = response.get_json()["total_price"]
    assert total_price == 54.95

def test_update_cart_with_invalid_quantity(client):
    client.post('/products/add', json={
        "name": "Test Product",
        "price": 10.99,
        "description": "A test product"
    })
    client.post('/cart/add', json={
        "product_id": "Test Product",
        "quantity": 2
    })
    response = client.post('/cart/update', json={"product_id": "Test Product", "quantity": -5})
    assert response.status_code == 400
    assert response.get_json() == {"error": "Quantity must be a positive integer"}