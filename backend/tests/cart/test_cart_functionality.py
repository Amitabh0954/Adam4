import pytest
from flask import Flask
from backend.app import create_app

@pytest.fixture
def app() -> Flask:
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    return app

@pytest.fixture
def client(app: Flask):
    return app.test_client()

def test_add_to_cart_logged_in(client):
    response = client.post('/cart/add', json={
        "product_id": "product123",
        "quantity": 1
    })
    assert response.status_code == 200
    assert response.get_json() == {"message": "Product added to cart successfully"}

def test_add_to_cart_guest(client):
    with client.session_transaction() as session:
        session['logged_in'] = False
    
    response = client.post('/cart/add', json={
        "product_id": "product123",
        "quantity": 1
    })
    assert response.status_code == 200
    assert response.get_json() == {"message": "Product added to cart successfully"}

def test_view_cart_logged_in(client):
    client.post('/cart/add', json={
        "product_id": "product123",
        "quantity": 1
    })
    
    response = client.get('/cart/view')
    assert response.status_code == 200
    cart = response.get_json()
    assert "product123" in cart["items"]

def test_view_cart_guest(client):
    with client.session_transaction() as session:
        session['cart'] = {"product123": 1}
    
    response = client.get('/cart/view')
    assert response.status_code == 200
    cart = response.get_json()
    assert cart == {"product123": 1}

def test_remove_from_cart_logged_in(client):
    client.post('/cart/add', json={
        "product_id": "product123",
        "quantity": 1
    })
    response = client.post('/cart/remove', json={
        "product_id": "product123"
    })
    assert response.status_code == 200
    assert response.get_json() == {"message": "Product removed from cart successfully"}

def test_remove_from_cart_guest(client):
    with client.session_transaction() as session:
        session['cart'] = {"product123": 1}
    
    response = client.post('/cart/remove', json={
        "product_id": "product123"
    })
    assert response.status_code == 200
    assert response.get_json() == {"message": "Product removed from cart successfully"}