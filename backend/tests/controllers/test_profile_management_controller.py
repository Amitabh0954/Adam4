```python  
"""
Tests for Profile Management Controller
"""

from fastapi.testclient import TestClient
from main import app
from backend.config.database import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models.account.user import User
from backend.models.base import Base
from passlib.context import CryptContext

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
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_test_user(db):
    user = User(email="testuser@example.com", hashed_password=pwd_context.hash("securepassword123"), name="Test User")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def test_update_profile():
    db = TestingSessionLocal()
    user = create_test_user(db)
    
    response = client.put(
        "/account/profile",
        params={"user_id": user.id},
        json={"email": "updatedemail@example.com", "name": "Updated User"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Profile updated successfully"
    assert data["user"]["email"] == "updatedemail@example.com"
    assert data["user"]["name"] == "Updated User"

def test_update_profile_email_already_registered():
    db = TestingSessionLocal()
    create_test_user(db)
    user = create_test_user(db)
    
    response = client.put(
        "/account/profile",
        params={"user_id": user.id},
        json={"email": "testuser@example.com"}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Email already registered"}
```