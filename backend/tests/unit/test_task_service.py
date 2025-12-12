"""
Unit tests for TaskService
"""
import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime
from fastapi import HTTPException

from source.services.task import TaskService
from source.schemas.task import params, responses
from source.db.models import Task


@pytest.mark.unit
class TestTaskService:
    """Test TaskService methods in isolation with mocked repositories."""
    
    @pytest.fixture
    def task_service(self, mock_task_repository):
        """Create TaskService instance with mocked repository."""
        return TaskService(task_repo=mock_task_repository)
    
    @pytest.fixture
    def mock_task_model(self):
        """Create a mock Task model."""
        task = MagicMock(spec=Task)
        task.id = 1
        task.description = "Test task"
        task.created_at = datetime.now()
        task.deadline = datetime(2025, 12, 31)
        task.priority_id = 1
        task.status_id = 1
        task.label_id = 1
        return task
    
    async def test_get_tasks_success(self, task_service, mock_task_repository, mock_task_model):
        """Test successful retrieval of tasks."""
        # Arrange
        get_params = params.GetTasks(label=None, status=None, priority=None)
        mock_task_repository.get_tasks = AsyncMock(return_value=[mock_task_model])
        
        # Act
        result = await task_service.get_tasks(get_params)
        
        # Assert
        assert isinstance(result, responses.GetTasks)
        assert len(result.items) == 1
        mock_task_repository.get_tasks.assert_called_once_with(get_params)
    
    async def test_get_tasks_empty(self, task_service, mock_task_repository):
        """Test get_tasks when no tasks exist."""
        # Arrange
        get_params = params.GetTasks(label=None, status=None, priority=None)
        mock_task_repository.get_tasks = AsyncMock(return_value=[])
        
        # Act
        result = await task_service.get_tasks(get_params)
        
        # Assert
        assert isinstance(result, responses.GetTasks)
        assert len(result.items) == 0
    
    async def test_create_task_success(self, task_service, mock_task_repository, mock_task_model):
        """Test successful task creation."""
        # Arrange
        create_params = params.CreateTask(
            description="New task",
            priority_id=1,
            status_id=1,
            label_id=1
        )
        mock_task_repository.new = AsyncMock(return_value=mock_task_model)
        
        # Act
        result = await task_service.create_task(create_params)
        
        # Assert
        assert isinstance(result, responses.Task)
        mock_task_repository.new.assert_called_once()
    
    async def test_create_task_failure(self, task_service, mock_task_repository):
        """Test task creation failure when repository returns None."""
        # Arrange
        create_params = params.CreateTask(
            description="New task",
            priority_id=1,
            status_id=1,
            label_id=1
        )
        mock_task_repository.new = AsyncMock(return_value=None)
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await task_service.create_task(create_params)
        
        assert exc_info.value.status_code == 500
    
    async def test_delete_task_success(self, task_service, mock_task_repository, mock_task_model):
        """Test successful task deletion."""
        # Arrange
        task_id = 1
        mock_task_repository.get_by_id = AsyncMock(return_value=mock_task_model)
        mock_task_repository.delete = AsyncMock(return_value=True)
        
        # Act
        result = await task_service.delete_task(task_id)
        
        # Assert
        assert isinstance(result, responses.Task)
        mock_task_repository.get_by_id.assert_called_once_with(task_id)
        mock_task_repository.delete.assert_called_once_with(mock_task_model)
    
    async def test_delete_task_not_found(self, task_service, mock_task_repository):
        """Test task deletion when task doesn't exist."""
        # Arrange
        task_id = 999
        mock_task_repository.get_by_id = AsyncMock(return_value=None)
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await task_service.delete_task(task_id)
        
        assert exc_info.value.status_code == 404
        assert "not found" in str(exc_info.value.detail).lower()
    
    async def test_delete_task_failure(self, task_service, mock_task_repository, mock_task_model):
        """Test task deletion failure."""
        # Arrange
        task_id = 1
        mock_task_repository.get_by_id = AsyncMock(return_value=mock_task_model)
        mock_task_repository.delete = AsyncMock(return_value=False)
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await task_service.delete_task(task_id)
        
        assert exc_info.value.status_code == 500
    
    async def test_update_task_success(self, task_service, mock_task_repository, mock_task_model):
        """Test successful task update."""
        # Arrange
        task_id = 1
        update_params = params.UpdateTask(
            task_id=task_id,
            description="Updated description",
            priority_id=2
        )
        
        updated_model = MagicMock(spec=Task)
        updated_model.id = task_id
        updated_model.description = "Updated description"
        
        mock_task_repository.get_by_id = AsyncMock(return_value=mock_task_model)
        mock_task_repository.update = AsyncMock(return_value=updated_model)
        
        # Act
        result = await task_service.update_task(update_params, task_id)
        
        # Assert
        assert isinstance(result, responses.Task)
        mock_task_repository.get_by_id.assert_called_once_with(task_id)
        mock_task_repository.update.assert_called_once()
    
    async def test_update_task_not_found(self, task_service, mock_task_repository):
        """Test task update when task doesn't exist."""
        # Arrange
        task_id = 999
        update_params = params.UpdateTask(
            task_id=task_id,
            description="Updated description"
        )
        mock_task_repository.get_by_id = AsyncMock(return_value=None)
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await task_service.update_task(update_params, task_id)
        
        assert exc_info.value.status_code == 404
    
    async def test_update_task_failure(self, task_service, mock_task_repository, mock_task_model):
        """Test task update failure."""
        # Arrange
        task_id = 1
        update_params = params.UpdateTask(
            task_id=task_id,
            description="Updated description"
        )
        mock_task_repository.get_by_id = AsyncMock(return_value=mock_task_model)
        mock_task_repository.update = AsyncMock(return_value=None)
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await task_service.update_task(update_params, task_id)
        
        assert exc_info.value.status_code == 500
