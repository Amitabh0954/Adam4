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

def test_total_price_logged_in(client):
    client.post('/products/add', json={
        "name": "Product A",
        "price": 10.0,
        "description": "Description A",
        "category": "Category A"
    })
    client.post('/products/add', json={
        "name": "Product B",
        "price": 20.0,
        "description": "Description B",
        "category": "Category B"
    })
    client.post('/cart/add', json={
        "product_id": "Product A",
        "quantity": 1
    })
    client.post('/cart/add', json={
        "product_id": "Product B",
        "quantity": 2
    })

    response = client.get('/cart/view')
    assert response.status_code == 200
    data = response.get_json()
    assert 'total_price' in data
    assert data['total_price'] == 50.0

def test_total_price_guest(client):
    with client.session_transaction() as session:
        session['cart'] = {"product123": 1}
    
    response = client.post('/cart/add', json={
        "product_id": "Product A",
        "quantity": 2
    })

    client.post('/products/add', json={
        "name": "Product A",
        "price": 10.0,
        "description": "Description A",
        "category": "Category A"
    })
    
    response = client.get('/cart/view')
    assert response.status_code == 200
    data = response.get_json()
    assert 'total_price' in data
    assert data['total_price'] == 20.0