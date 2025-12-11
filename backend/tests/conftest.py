"""
Global pytest fixtures for all tests
"""
import asyncio
import os
from typing import AsyncGenerator, Generator
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
from faker import Faker

# Set test environment
os.environ["APP_ENV"] = "test"

from source.db.models.base import Base
from source.db.models import Task, Priority, Status, Label, User
from source.db.database import get_session
from source.api.app import app


# Test database URL
TEST_DATABASE_URL = "postgresql+asyncpg://test_user:test_password@localhost:5433/test_taskmanager"

# Create test engine
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    poolclass=NullPool,
    echo=False,
)

test_async_session_maker = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

fake = Faker()


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def test_db() -> AsyncGenerator[None, None]:
    """Create test database tables before each test and drop after."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield
    
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def test_session(test_db) -> AsyncGenerator[AsyncSession, None]:
    """Create a test database session."""
    async with test_async_session_maker() as session:
        yield session


@pytest.fixture(scope="function")
async def async_client(test_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create an async HTTP client for API testing."""
    
    async def override_get_session():
        yield test_session
    
    app.dependency_overrides[get_session] = override_get_session
    
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        yield client
    
    app.dependency_overrides.clear()


# Sample data fixtures

@pytest.fixture
def sample_priority_data() -> dict:
    """Sample priority data for testing."""
    return {
        "name": "High",
        "description": "High priority tasks"
    }


@pytest.fixture
def sample_status_data() -> dict:
    """Sample status data for testing."""
    return {
        "name": "In Progress",
        "description": "Tasks currently being worked on"
    }


@pytest.fixture
def sample_label_data() -> dict:
    """Sample label data for testing."""
    return {
        "name": "Bug",
        "description": "Bug-related tasks"
    }


@pytest.fixture
def sample_task_data() -> dict:
    """Sample task data for testing."""
    return {
        "description": "Test task description",
        "deadline": "2025-12-31T23:59:59"
    }


@pytest.fixture
async def test_priority(test_session: AsyncSession, sample_priority_data: dict) -> Priority:
    """Create a test priority in the database."""
    priority = Priority(**sample_priority_data)
    test_session.add(priority)
    await test_session.commit()
    await test_session.refresh(priority)
    return priority


@pytest.fixture
async def test_status(test_session: AsyncSession, sample_status_data: dict) -> Status:
    """Create a test status in the database."""
    status = Status(**sample_status_data)
    test_session.add(status)
    await test_session.commit()
    await test_session.refresh(status)
    return status


@pytest.fixture
async def test_label(test_session: AsyncSession, sample_label_data: dict) -> Label:
    """Create a test label in the database."""
    label = Label(**sample_label_data)
    test_session.add(label)
    await test_session.commit()
    await test_session.refresh(label)
    return label


@pytest.fixture
async def test_task(
    test_session: AsyncSession,
    test_priority: Priority,
    test_status: Status,
    test_label: Label,
    sample_task_data: dict
) -> Task:
    """Create a test task in the database."""
    from datetime import datetime
    
    task = Task(
        description=sample_task_data["description"],
        deadline=datetime.fromisoformat(sample_task_data["deadline"]),
        created_at=datetime.now(),
        priority_id=test_priority.id,
        status_id=test_status.id,
        label_id=test_label.id,
    )
    test_session.add(task)
    await test_session.commit()
    await test_session.refresh(task)
    return task


# Mock fixtures for unit tests

@pytest.fixture
def mock_task_repository(mocker):
    """Mock task repository for unit tests."""
    from db.repositories import TaskRepository
    mock_repo = mocker.MagicMock(spec=TaskRepository)
    return mock_repo


@pytest.fixture
def mock_priority_repository(mocker):
    """Mock priority repository for unit tests."""
    from db.repositories import PriorityRepository
    mock_repo = mocker.MagicMock(spec=PriorityRepository)
    return mock_repo


@pytest.fixture
def mock_status_repository(mocker):
    """Mock status repository for unit tests."""
    from db.repositories import StatusRepository
    mock_repo = mocker.MagicMock(spec=StatusRepository)
    return mock_repo


@pytest.fixture
def mock_label_repository(mocker):
    """Mock label repository for unit tests."""
    from db.repositories import LabelRepository
    mock_repo = mocker.MagicMock(spec=LabelRepository)
    return mock_repo
