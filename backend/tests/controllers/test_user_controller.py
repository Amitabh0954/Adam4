```python  
"""
Tests for User Registration Controller
"""

from fastapi.testclient import TestClient
from main import app
from backend.config.database import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models.account.user import User
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

def test_register_user():
    response = client.post(
        "/account/register",
        json={"email": "testuser@example.com", "password": "securepassword123"},
    )
    assert response.status_code == 200
    assert response.json() == "User registered successfully"

def test_register_user_duplicate():
    db = TestingSessionLocal()
    user = User(email="testuser@example.com", hashed_password="hashedpassword123")
    db.add(user)
    db.commit()
    db.refresh(user)
    
    response = client.post(
        "/account/register",
        json={"email": "testuser@example.com", "password": "securepassword123"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Email already registered"}
```