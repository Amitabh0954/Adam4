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
    client.post('/category/add', json={
        "name": "Electronics"
    })
    response = client.post('/products/add', json={
        "name": "Test Product",
        "price": 10.99,
        "description": "A test product",
        "categories": ["Electronics"]
    })
    assert response.status_code == 201
    product = response.get_json()
    assert product["name"] == "Test Product"
    assert product["price"] == 10.99
    assert product["description"] == "A test product"
    assert "Electronics" in product["categories"]

def test_add_product_without_category(client):
    response = client.post('/products/add', json={
        "name": "Test Product",
        "price": 10.99,
        "description": "A test product"
    })
    assert response.status_code == 400
    assert response.get_json() == {"error": "At least one category is required"}

def test_add_product_with_nonexistent_category(client):
    response = client.post('/products/add', json={
        "name": "Test Product",
        "price": 10.99,
        "description": "A test product",
        "categories": ["Nonexistent"]
    })
    assert response.status_code == 400
    assert "Category Nonexistent does not exist" in response.get_json()["error"]

def test_list_products(client):
    client.post('/category/add', json={
        "name": "Electronics"
    })
    client.post('/products/add', json={
        "name": "Test Product 1",
        "price": 10.99,
        "description": "First test product",
        "categories": ["Electronics"]
    })
    client.post('/products/add', json={
        "name": "Test Product 2",
        "price": 15.99,
        "description": "Second test product",
        "categories": ["Electronics"]
    })

    response = client.get('/products/list')
    assert response.status_code == 200
    products = response.get_json()
    assert len(products) == 2
    assert products[0]["name"] == "Test Product 1"
    assert products[0]["price"] == 10.99
    assert products[0]["description"] == "First test product"
    assert "Electronics" in products[0]["categories"]
    assert products[1]["name"] == "Test Product 2"
    assert products[1]["price"] == 15.99
    assert products[1]["description"] == "Second test product"
    assert "Electronics" in products[1]["categories"]

def test_update_product(client):
    client.post('/category/add', json={
        "name": "Electronics"
    })
    client.post('/products/add', json={
        "name": "Test Product",
        "price": 10.99,
        "description": "A test product",
        "categories": ["Electronics"]
    })

    response = client.put('/products/update/Test Product', json={
        "price": 12.99,
        "description": "An updated test product",
        "categories": ["Electronics"]
    })
    assert response.status_code == 200
    product = response.get_json()
    assert product["name"] == "Test Product"
    assert product["price"] == 12.99
    assert product["description"] == "An updated test product"
    assert "Electronics" in product["categories"]

def test_update_product_with_nonexistent_category(client):
    client.post('/category/add', json={
        "name": "Electronics"
    })
    client.post('/products/add', json={
        "name": "Test Product",
        "price": 10.99,
        "description": "A test product",
        "categories": ["Electronics"]
    })

    response = client.put('/products/update/Test Product', json={
        "price": 12.99,
        "description": "An updated test product",
        "categories": ["Nonexistent"]
    })
    assert response.status_code == 400
    assert "Category Nonexistent does not exist" in response.get_json()["error"]

def test_delete_product(client):
    client.post('/category/add', json={
        "name": "Electronics"
    })
    client.post('/products/add', json={
        "name": "Test Product",
        "price": 10.99,
        "description": "A test product",
        "categories": ["Electronics"]
    })

    response = client.delete('/products/delete/Test Product', query_string={"confirm": "yes"})
    assert response.status_code == 200
    assert response.get_json() == {"message": "Product deleted successfully"}

def test_delete_product_without_confirmation(client):
    client.post('/category/add', json={
        "name": "Electronics"
    })
    client.post('/products/add', json={
        "name": "Test Product",
        "price": 10.99,
        "description": "A test product",
        "categories": ["Electronics"]
    })

    response = client.delete('/products/delete/Test Product')
    assert response.status_code == 400
    assert response.get_json() == {"error": "Confirmation required to delete product"}

def test_delete_non_existent_product(client):
    response = client.delete('/products/delete/Non Existent Product', query_string={"confirm": "yes"})
    assert response.status_code == 404
    assert response.get_json() == {"error": "Product not found"}

def test_search_products(client):
    client.post('/category/add', json={
        "name": "Category A"
    })
    client.post('/category/add', json={
        "name": "Category B"
    })
    client.post('/products/add', json={
        "name": "Test Product 1",
        "price": 10.99,
        "description": "First test product",
        "categories": ["Category A"]
    })
    client.post('/products/add', json={
        "name": "Test Product 2",
        "price": 15.99,
        "description": "Second test product",
        "categories": ["Category B"]
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