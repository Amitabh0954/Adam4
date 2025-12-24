```python  
"""
Tests for User Login Controller
"""

from fastapi.testclient import TestClient
from main import app
from backend.config.database import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models.account.user import User
from backend.models.base import Base
from jose import jwt
from backend.config.settings import settings
from datetime import datetime, timedelta

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

def create_test_user(db):
    user = User(email="testuser@example.com", hashed_password=pwd_context.hash("securepassword123"))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def test_login_user():
    db = TestingSessionLocal()
    create_test_user(db)
    
    response = client.post(
        "/account/login",
        json={"email": "testuser@example.com", "password": "securepassword123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert datetime.strptime(data["expires"], "%Y-%m-%dT%H:%M:%S.%f") > datetime.utcnow()

def test_invalid_login():
    db = TestingSessionLocal()
    create_test_user(db)
    
    response = client.post(
        "/account/login",
        json={"email": "testuser@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid email or password"}
```