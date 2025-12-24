```python  
"""
Tests for Password Recovery Controller
"""

from fastapi.testclient import TestClient
from main import app
from backend.config.database import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models.account.user import User
from backend.models.base import Base
from backend.services.account.password_recovery_service import PasswordRecoveryService

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

def test_password_reset():
    db = TestingSessionLocal()
    user = create_test_user(db)
    
    response = client.post(
        "/account/password-reset",
        json={"email": "testuser@example.com"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "token" in data

    reset_token = data.split(": ")[-1]
    new_password = "newsecurepassword123"
    
    response = client.post(
        "/account/password-reset-confirm",
        json={"token": reset_token, "new_password": new_password},
    )
    assert response.status_code == 200
    assert response.json() == "Password reset successfully"

    service = PasswordRecoveryService(UserRepository(db))
    user = service.verify_reset_token(reset_token)
    assert user.hashed_password != pwd_context.hash("newsecurepassword123")
```