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

def test_search_products(client):
    client.post('/products/add', json={
        "name": "Search Test Product A",
        "price": 10.99,
        "description": "Description of product A",
        "category": "Category A"
    })
    client.post('/products/add', json={
        "name": "Search Test Product B",
        "price": 20.99,
        "description": "Description of product B",
        "category": "Category B"
    })

    response = client.get('/products/search', query_string={
        "query": "Test",
        "page": 1,
        "per_page": 10
    })
    assert response.status_code == 200
    data = response.get_json()
    assert len(data["results"]) > 0
    assert data["total"] >= 2

def test_search_no_results(client):
    response = client.get('/products/search', query_string={
        "query": "Nonexistent",
        "page": 1,
        "per_page": 10
    })
    assert response.status_code == 200
    data = response.get_json()
    assert len(data["results"]) == 0
    assert data["total"] == 0

def test_search_pagination(client):
    for i in range(15):
        client.post('/products/add', json={
            "name": f"Product {i}",
            "price": 10.99 + i,
            "description": f"Description of product {i}",
            "category": f"Category {i % 3}"
        })
    
    response = client.get('/products/search', query_string={
        "query": "Product",
        "page": 2,
        "per_page": 5
    })
    assert response.status_code == 200
    data = response.get_json()
    assert len(data["results"]) == 5
    assert data["total"] == 15
    assert data["page"] == 2
    assert data["per_page"] == 5