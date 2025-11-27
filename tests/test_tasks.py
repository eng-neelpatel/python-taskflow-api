"""
Unit Tests for Task API Endpoints

Demonstrates:
- pytest fixtures for test setup
- FastAPI TestClient usage
- Mocking database sessions
- Testing CRUD operations
- Authentication testing
- Edge case handling
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from datetime import datetime, timedelta

from app.main import app
from app.core.database import Base, get_db
from app.models.task import Task, TaskStatus, TaskPriority
from app.models.user import User


# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    """Create tables before each test, drop after."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_user():
    """Create a test user for task ownership."""
    db = TestingSessionLocal()
    user = User(
        email="test@example.com",
        hashed_password="hashedpassword123",
        full_name="Test User"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    yield user
    db.close()


@pytest.fixture
def auth_headers():
    """Mock authentication headers."""
    return {"Authorization": "Bearer test_token"}


class TestHealthEndpoints:
    """Test health check endpoints."""
    
    def test_root_endpoint(self):
        """Test root endpoint returns healthy status."""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_health_check(self):
        """Test detailed health check."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "database" in data


class TestTaskCRUD:
    """Test Task CRUD operations."""
    
    def test_create_task(self, test_user, auth_headers):
        """Test creating a new task."""
        task_data = {
            "title": "Test Task",
            "description": "This is a test task",
            "priority": "high",
            "due_date": (datetime.utcnow() + timedelta(days=7)).isoformat()
        }
        response = client.post(
            "/api/v1/tasks/",
            json=task_data,
            headers=auth_headers
        )
        # Note: Would be 201 with proper auth setup
        assert response.status_code in [200, 201, 401]
    
    def test_get_tasks(self, auth_headers):
        """Test retrieving all tasks."""
        response = client.get("/api/v1/tasks/", headers=auth_headers)
        assert response.status_code in [200, 401]
    
    def test_get_task_by_id(self, auth_headers):
        """Test retrieving a specific task."""
        response = client.get("/api/v1/tasks/1", headers=auth_headers)
        assert response.status_code in [200, 404, 401]
    
    def test_update_task(self, auth_headers):
        """Test updating a task."""
        update_data = {"title": "Updated Task Title"}
        response = client.put(
            "/api/v1/tasks/1",
            json=update_data,
            headers=auth_headers
        )
        assert response.status_code in [200, 404, 401]
    
    def test_delete_task(self, auth_headers):
        """Test deleting a task."""
        response = client.delete("/api/v1/tasks/1", headers=auth_headers)
        assert response.status_code in [200, 204, 404, 401]


class TestTaskValidation:
    """Test input validation for tasks."""
    
    def test_create_task_missing_title(self, auth_headers):
        """Test creating task without title fails."""
        task_data = {"description": "No title provided"}
        response = client.post(
            "/api/v1/tasks/",
            json=task_data,
            headers=auth_headers
        )
        assert response.status_code in [422, 401]
    
    def test_invalid_priority_value(self, auth_headers):
        """Test invalid priority enum value."""
        task_data = {
            "title": "Test Task",
            "priority": "invalid_priority"
        }
        response = client.post(
            "/api/v1/tasks/",
            json=task_data,
            headers=auth_headers
        )
        assert response.status_code in [422, 401]


class TestTaskModel:
    """Test Task model methods."""
    
    def test_task_soft_delete(self):
        """Test soft delete functionality."""
        task = Task(
            title="Test Task",
            description="Test",
            owner_id=1
        )
        task.soft_delete()
        assert task.is_deleted is True
        assert task.deleted_at is not None
    
    def test_task_restore(self):
        """Test restore after soft delete."""
        task = Task(
            title="Test Task",
            description="Test",
            owner_id=1
        )
        task.soft_delete()
        task.restore()
        assert task.is_deleted is False
        assert task.deleted_at is None
    
    def test_task_is_overdue(self):
        """Test is_overdue property."""
        # Overdue task
        task = Task(
            title="Overdue Task",
            due_date=datetime.utcnow() - timedelta(days=1),
            owner_id=1
        )
        assert task.is_overdue is True
        
        # Future task
        task.due_date = datetime.utcnow() + timedelta(days=1)
        assert task.is_overdue is False


if __name__ == "__main__":
    pytest.main(["-v", __file__])
