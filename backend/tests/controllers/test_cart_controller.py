```python  
"""
Tests for Cart Controller
"""

from fastapi.testclient import TestClient
from main import app
from backend.config.database import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models.catalog.product import Product
from backend.models.cart.shopping_cart import ShoppingCart, CartItem
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

def create_test_product(db, name="Test Product", price=10.0):
    product = Product(name=name, description="This is a test product", price=price, category_id=1)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def test_add_product_to_cart():
    db = TestingSessionLocal()
    product = create_test_product(db)
    
    response = client.post("/cart/add", json={"product_id": product.id, "user_id": 1, "quantity": 2})
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Product added to cart"
    assert data["cart_item"]["product_id"] == product.id
    assert data["cart_item"]["quantity"] == 2

def test_remove_product_from_cart():
    db = TestingSessionLocal()
    product = create_test_product(db)
    
    cart = ShoppingCart(user_id=1)
    db.add(cart)
    db.commit()
    db.refresh(cart)
    
    cart_item = CartItem(cart_id=cart.id, product_id=product.id, quantity=1)
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    
    response = client.post("/cart/remove", json={"product_id": product.id, "user_id": 1})
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Product removed from cart"

def test_modify_product_quantity():
    db = TestingSessionLocal()
    product = create_test_product(db)
    
    cart = ShoppingCart(user_id=1)
    db.add(cart)
    db.commit()
    db.refresh(cart)
    
    cart_item = CartItem(cart_id=cart.id, product_id=product.id, quantity=1)
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    
    response = client.post("/cart/modify_quantity", json={"product_id": product.id, "user_id": 1, "quantity": 5})
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Product quantity updated"
    assert data["quantity"] == 5

def test_modify_product_quantity_invalid():
    response = client.post("/cart/modify_quantity", json={"product_id": 1, "user_id": 1, "quantity": 0})
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Quantity must be a positive integer"
```