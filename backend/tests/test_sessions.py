import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from app.main import app
from app.database.database import get_db, Base

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override get_db dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create test client
client = TestClient(app)

@pytest.fixture(scope="module")
def setup_database():
    # Create tables
    Base.metadata.create_all(bind=engine)
    yield
    # Drop tables after tests
    Base.metadata.drop_all(bind=engine)

def test_create_session(setup_database):
    """Test creating a new session"""
    session_data = {
        "date": "2023-12-13T18:00:00",
        "location": "Casino Royal",
        "sb_size": 1.0,
        "bb_size": 2.0,
        "buy_in": 200.0,
        "cash_out": 350.0,
        "hours": 4.5,
        "notes": "Great session with loose players"
    }
    
    response = client.post("/sessions/", json=session_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["location"] == session_data["location"]
    assert data["sb_size"] == session_data["sb_size"]
    assert data["bb_size"] == session_data["bb_size"]
    assert data["buy_in"] == session_data["buy_in"]
    assert data["cash_out"] == session_data["cash_out"]
    assert data["hours"] == session_data["hours"]
    assert data["net_profit"] == 150.0  # 350 - 200
    assert abs(data["bb_per_hour"] - 16.67) < 0.01  # (150/2)/4.5 ≈ 16.67
    assert "id" in data

def test_get_sessions(setup_database):
    """Test retrieving all sessions"""
    response = client.get("/sessions/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_session_by_id(setup_database):
    """Test retrieving a specific session"""
    # First create a session
    session_data = {
        "date": "2023-12-14T20:00:00",
        "location": "Home Game",
        "sb_size": 0.5,
        "bb_size": 1.0,
        "buy_in": 100.0,
        "cash_out": 85.0,
        "hours": 3.0
    }
    
    create_response = client.post("/sessions/", json=session_data)
    session_id = create_response.json()["id"]
    
    # Get the session
    response = client.get(f"/sessions/{session_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["location"] == session_data["location"]
    assert data["net_profit"] == -15.0  # 85 - 100

def test_create_session_validation(setup_database):
    """Test session creation with invalid data"""
    # Test negative buy_in
    invalid_data = {
        "date": "2023-12-13T18:00:00",
        "location": "Test Casino",
        "sb_size": 1.0,
        "bb_size": 2.0,
        "buy_in": -100.0,  # Invalid: negative
        "cash_out": 200.0,
        "hours": 4.0
    }
    
    response = client.post("/sessions/", json=invalid_data)
    assert response.status_code == 422  # Validation error
    
    # Test negative sb_size
    invalid_sb_data = {
        "date": "2023-12-13T18:00:00",
        "location": "Test Casino",
        "sb_size": -1.0,  # Invalid: negative
        "bb_size": 2.0,
        "buy_in": 100.0,
        "cash_out": 200.0,
        "hours": 4.0
    }
    
    response = client.post("/sessions/", json=invalid_sb_data)
    assert response.status_code == 422

def test_delete_session(setup_database):
    """Test deleting a session"""
    # Create a session first
    session_data = {
        "date": "2023-12-15T19:00:00",
        "location": "Delete Test Casino",
        "sb_size": 2.0,
        "bb_size": 5.0,
        "buy_in": 500.0,
        "cash_out": 600.0,
        "hours": 2.0
    }
    
    create_response = client.post("/sessions/", json=session_data)
    session_id = create_response.json()["id"]
    
    # Delete the session
    response = client.delete(f"/sessions/{session_id}")
    assert response.status_code == 204
    
    # Verify it's deleted
    get_response = client.get(f"/sessions/{session_id}")
    assert get_response.status_code == 404 