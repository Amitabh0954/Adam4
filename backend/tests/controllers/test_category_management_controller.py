```python  
"""
Tests for Category Management Controller
"""

from fastapi.testclient import TestClient
from main import app
from backend.config.database import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
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

def test_create_category():
    response = client.post(
        "/catalog/categories",
        json={"name": "Test Category"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Category created successfully"
    assert data["category"]["name"] == "Test Category"
    assert data["category"]["parent_id"] is None

def test_create_category_with_parent():
    db = TestingSessionLocal()
    parent_category = Category(name="Parent Category")
    db.add(parent_category)
    db.commit()
    db.refresh(parent_category)
    
    response = client.post(
        "/catalog/categories",
        json={"name": "Child Category", "parent_id": parent_category.id},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Category created successfully"
    assert data["category"]["name"] == "Child Category"
    assert data["category"]["parent_id"] == parent_category.id

def test_create_category_with_invalid_parent():
    response = client.post(
        "/catalog/categories",
        json={"name": "Child Category", "parent_id": 9999},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Parent category not found"}

def test_list_categories():
    response = client.get("/catalog/categories")
    assert response.status_code == 200
    data = response.json()
    assert "categories" in data
```