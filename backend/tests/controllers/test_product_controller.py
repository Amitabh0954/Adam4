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
        "description": "A test product"
    })
    assert response.status_code == 201
    product = response.get_json()
    assert product["name"] == "Test Product"
    assert product["price"] == 10.99
    assert product["description"] == "A test product"

def test_add_product_with_existing_name(client):
    client.post('/products/add', json={
        "name": "Test Product",
        "price": 10.99,
        "description": "A test product"
    })
    response = client.post('/products/add', json={
        "name": "Test Product",
        "price": 15.99,
        "description": "Another test product"
    })
    assert response.status_code == 400
    assert response.get_json() == {"error": "Product name is already taken"}

def test_add_product_with_negative_price(client):
    response = client.post('/products/add', json={
        "name": "Test Product",
        "price": -10.99,
        "description": "A test product"
    })
    assert response.status_code == 400
    assert response.get_json() == {"error": "Price must be a positive number"}

def test_add_product_with_missing_fields(client):
    response = client.post('/products/add', json={
        "name": "Test Product",
        "price": 10.99
    })
    assert response.status_code == 400
    assert response.get_json() == {"error": "Name, description, and price are required"}

def test_list_products(client):
    client.post('/products/add', json={
        "name": "Test Product 1",
        "price": 10.99,
        "description": "First test product"
    })
    client.post('/products/add', json={
        "name": "Test Product 2",
        "price": 15.99,
        "description": "Second test product"
    })

    response = client.get('/products/list')
    assert response.status_code == 200
    products = response.get_json()
    assert len(products) == 2
    assert products[0]["name"] == "Test Product 1"
    assert products[0]["price"] == 10.99
    assert products[0]["description"] == "First test product"
    assert products[1]["name"] == "Test Product 2"
    assert products[1]["price"] == 15.99
    assert products[1]["description"] == "Second test product"

def test_update_product(client):
    client.post('/products/add', json={
        "name": "Test Product",
        "price": 10.99,
        "description": "A test product"
    })

    response = client.put('/products/update/Test Product', json={
        "price": 12.99,
        "description": "An updated test product"
    })
    assert response.status_code == 200
    product = response.get_json()
    assert product["name"] == "Test Product"
    assert product["price"] == 12.99
    assert product["description"] == "An updated test product"

def test_update_product_with_invalid_price(client):
    client.post('/products/add', json={
        "name": "Test Product",
        "price": 10.99,
        "description": "A test product"
    })

    response = client.put('/products/update/Test Product', json={
        "price": "invalid_price"
    })
    assert response.status_code == 400
    assert response.get_json() == {"error": "Price must be a numeric value"}

def test_update_product_with_empty_description(client):
    client.post('/products/add', json={
        "name": "Test Product",
        "price": 10.99,
        "description": "A test product"
    })

    response = client.put('/products/update/Test Product', json={
        "description": ""
    })
    assert response.status_code == 400
    assert response.get_json() == {"error": "Description cannot be empty"}

def test_update_non_existent_product(client):
    response = client.put('/products/update/Non Existent Product', json={
        "price": 12.99,
        "description": "An updated test product"
    })
    assert response.status_code == 404
    assert response.get_json() == {"error": "Product not found"}

def test_delete_product(client):
    client.post('/products/add', json={
        "name": "Test Product",
        "price": 10.99,
        "description": "A test product"
    })

    response = client.delete('/products/delete/Test Product', query_string={"confirm": "yes"})
    assert response.status_code == 200
    assert response.get_json() == {"message": "Product deleted successfully"}

def test_delete_product_without_confirmation(client):
    client.post('/products/add', json={
        "name": "Test Product",
        "price": 10.99,
        "description": "A test product"
    })

    response = client.delete('/products/delete/Test Product')
    assert response.status_code == 400
    assert response.get_json() == {"error": "Confirmation required to delete product"}

def test_delete_non_existent_product(client):
    response = client.delete('/products/delete/Non Existent Product', query_string={"confirm": "yes"})
    assert response.status_code == 404
    assert response.get_json() == {"error": "Product not found"}

def test_search_products(client):
    client.post('/products/add', json={
        "name": "Test Product 1",
        "price": 10.99,
        "description": "First test product",
        "category": "Category A"
    })
    client.post('/products/add', json={
        "name": "Test Product 2",
        "price": 15.99,
        "description": "Second test product",
        "category": "Category B"
    })

    response = client.get('/products/search', query_string={"query": "Category", "page": 1, "per_page": 1})
    assert response.status_code == 200
    search_results = response.get_json()
    assert search_results["total"] == 2
    assert len(search_results["products"]) == 1
    assert search_results["products"][0]["name"] == "Test Product 1"

    response = client.get('/products/search', query_string={"query": "Second", "page": 1, "per_page": 10})
    assert response.status_code == 200
    search_results = response.get_json()
    assert search_results["total"] == 1
    assert search_results["products"][0]["name"] == "Test Product 2"