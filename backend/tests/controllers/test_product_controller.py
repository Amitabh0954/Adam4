```python  
"""
Tests for Product Management Controller
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

def test_add_product():
    db = TestingSessionLocal()
    category = create_test_category(db)
    
    response = client.post(
        "/catalog/products",
        json={"name": "Test Product", "description": "This is a test product", "price": 10.0, "category_id": category.id},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Product added successfully"
    assert data["product"]["name"] == "Test Product"
    assert data["product"]["description"] == "This is a test product"
    assert data["product"]["price"] == 10.0
    assert data["product"]["category_id"] == category.id

def test_add_product_name_already_exists():
    db = TestingSessionLocal()
    category = create_test_category(db)
    product = Product(name="Test Product", description="This is a test product", price=10.0, category_id=category.id)
    db.add(product)
    db.commit()
    db.refresh(product)
    
    response = client.post(
        "/catalog/products",
        json={"name": "Test Product", "description": "This is another test product", "price": 15.0, "category_id": category.id},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Product name already exists"}
```