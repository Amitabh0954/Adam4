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

def test_update_product(client):
    client.post('/products/add', json={
        "name": "Update Test Product",
        "price": 10.99,
        "description": "Initial description",
        "category": "Test Category"
    })

    response = client.put('/products/update', json={
        "name": "Update Test Product",
        "price": 20.99,
        "description": "Updated description",
        "category": "Updated Category"
    })
    assert response.status_code == 200
    assert response.get_json() == {"message": "Product updated successfully"}

def test_update_nonexistent_product(client):
    response = client.put('/products/update', json={
        "name": "Nonexistent Product",
        "price": 10.99,
        "description": "Description",
        "category": "Category"
    })
    assert response.status_code == 404
    assert response.get_json() == {"error": "Product not found"}

def test_update_product_with_invalid_price(client):
    client.post('/products/add', json={
        "name": "Invalid Price Update Product",
        "price": 10.99,
        "description": "Valid description",
        "category": "Test Category"
    })

    response = client.put('/products/update', json={
        "name": "Invalid Price Update Product",
        "price": -10.99,
        "description": "Valid description",
        "category": "Test Category"
    })
    assert response.status_code == 400
    assert response.get_json() == {"error": "Product price must be a positive number"}

def test_update_product_with_empty_description(client):
    client.post('/products/add', json={
        "name": "Empty Description Update Product",
        "price": 10.99,
        "description": "Valid description",
        "category": "Test Category"
    })

    response = client.put('/products/update', json={
        "name": "Empty Description Update Product",
        "price": 10.99,
        "description": "",
        "category": "Test Category"
    })
    assert response.status_code == 400
    assert response.get_json() == {"error": "Product description cannot be empty"}