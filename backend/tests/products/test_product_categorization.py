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

def test_add_category(client):
    response = client.post('/products/add_category', json={
        "name": "Electronics"
    })
    assert response.status_code == 201
    assert response.get_json() == {"message": "Category added successfully"}

def test_add_subcategory(client):
    client.post('/products/add_category', json={
        "name": "Electronics"
    })
    response = client.post('/products/add_category', json={
        "name": "Mobile Phones",
        "parent": "Electronics"
    })
    assert response.status_code == 201
    assert response.get_json() == {"message": "Category added successfully"}

def test_get_all_categories(client):
    client.post('/products/add_category', json={
        "name": "Electronics"
    })
    client.post('/products/add_category', json={
        "name": "Mobile Phones",
        "parent": "Electronics"
    })
    response = client.get('/products/categories')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) >= 2
    assert data[0]["name"] == "Electronics"
    assert data[1]["name"] == "Mobile Phones"
    assert "Mobile Phones" in data[0]["children"]