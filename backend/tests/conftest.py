"""Test configuration and fixtures"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.app.db.database import Base, get_db
from backend.main import app

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def test_db():
    """Create test database"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session(test_db):
    """Get database session"""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(db_session):
    """Get test client"""
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


@pytest.fixture
def auth_headers(client):
    """Get authentication headers"""
    # Create test user
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpassword123",
            "role": "admin"
        }
    )
    
    # Login
    response = client.post(
        "/api/v1/auth/login?email=test@example.com&password=testpassword123"
    )
    
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
