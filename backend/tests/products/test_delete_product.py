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

def test_delete_product(client):
    client.post('/products/add', json={
        "name": "Delete Test Product",
        "price": 10.99,
        "description": "Description of product to delete",
        "category": "Test Category"
    })

    response = client.delete('/products/delete', json={
        "name": "Delete Test Product"
    })
    assert response.status_code == 200
    assert response.get_json() == {"message": "Product deleted successfully"}

    response = client.delete('/products/delete', json={
        "name": "Delete Test Product"
    })
    assert response.status_code == 404
    assert response.get_json() == {"error": "Product not found"}

def test_delete_nonexistent_product(client):
    response = client.delete('/products/delete', json={
        "name": "Nonexistent Product"
    })
    assert response.status_code == 404
    assert response.get_json() == {"error": "Product not found"}