```python  
"""
Tests for Product Search Controller
"""

from fastapi.testclient import TestClient
from main import app
from backend.config.database import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models.catalog.product import Product
from backend.models.catalog.category import Category
from backend.models.base import Base

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def create_test_category(db):
    category = Category(name="Test Category")
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

def create_test_product(db, category_id, name):
    product = Product(name=name, description="This is a test product", price=10.0, category_id=category_id)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def test_search_products():
    db = TestingSessionLocal()
    category = create_test_category(db)
    create_test_product(db, category.id, "Product 1")
    create_test_product(db, category.id, "Product 2")
    create_test_product(db, category.id, "Another Product")
    
    response = client.get(
        "/catalog/products/search",
        params={"query": "Product", "page": 1, "per_page": 2},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["products"]) == 2
    assert data["products"][0]["name"] in ["Product 1", "Product 2"]
    assert data["products"][1]["name"] in ["Product 1", "Product 2"]

def test_search_no_results():
    response = client.get(
        "/catalog/products/search",
        params={"query": "Nonexistent Product", "page": 1, "per_page": 2},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["products"]) == 0
```