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
    cart = response.get_json()
    assert "Test Product" in cart["items"]
    assert cart["items"]["Test Product"] == 2

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
    response = client.post('/cart/remove', json={"product_id": "Test Product"})
    assert response.status_code == 200
    assert response.get_json() == {"message": "Product removed from cart successfully"}
    response = client.get('/cart/view')
    assert response.status_code == 200
    cart = response.get_json()
    assert "items" in cart
    assert "Test Product" not in cart["items"]