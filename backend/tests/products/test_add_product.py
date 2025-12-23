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

def test_add_product(client):
    response = client.post('/products/add', json={
        "name": "Test Product",
        "price": 10.99,
        "description": "A test product",
        "category": "Test Category"
    })
    assert response.status_code == 201
    assert response.get_json() == {"message": "Product added successfully"}

def test_add_product_with_existing_name(client):
    client.post('/products/add', json={
        "name": "Unique Product",
        "price": 15.99,
        "description": "Unique product",
        "category": "Test Category"
    })

    response = client.post('/products/add', json={
        "name": "Unique Product",
        "price": 15.99,
        "description": "Another product with same name",
        "category": "Test Category"
    })
    assert response.status_code == 400
    assert response.get_json() == {"error": "Product name must be unique"}

def test_add_product_with_invalid_price(client):
    response = client.post('/products/add', json={
        "name": "Invalid Price Product",
        "price": -5.99,
        "description": "Product with invalid price",
        "category": "Test Category"
    })
    assert response.status_code == 400
    assert response.get_json() == {"error": "Product price must be a positive number"}

def test_add_product_with_empty_description(client):
    response = client.post('/products/add', json={
        "name": "No Description Product",
        "price": 5.99,
        "description": "",
        "category": "Test Category"
    })
    assert response.status_code == 400
    assert response.get_json() == {"error": "Product description cannot be empty"}