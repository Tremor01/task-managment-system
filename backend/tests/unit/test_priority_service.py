"""
Unit tests for PriorityService
"""
import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException

from services.priority import PriorityService
from schemas.priority import params, responses
from db.models import Priority


@pytest.mark.unit
class TestPriorityService:
    """Test PriorityService methods in isolation with mocked repositories."""
    
    @pytest.fixture
    def priority_service(self, mock_priority_repository):
        """Create PriorityService instance with mocked repository."""
        return PriorityService(priority_repo=mock_priority_repository)
    
    @pytest.fixture
    def mock_priority_model(self):
        """Create a mock Priority model."""
        priority = MagicMock(spec=Priority)
        priority.id = 1
        priority.name = "High"
        priority.description = "High priority"
        return priority
    
    async def test_get_priorities_success(self, priority_service, mock_priority_repository, mock_priority_model):
        """Test successful retrieval of priorities."""
        # Arrange
        mock_priority_repository.select_all = AsyncMock(return_value=[mock_priority_model])
        
        # Act
        result = await priority_service.get_priorities()
        
        # Assert
        assert isinstance(result, responses.GetPriorities)
        assert len(result.items) == 1
        mock_priority_repository.select_all.assert_called_once()
    
    async def test_get_priorities_empty(self, priority_service, mock_priority_repository):
        """Test get_priorities when no priorities exist."""
        # Arrange
        mock_priority_repository.select_all = AsyncMock(return_value=[])
        
        # Act
        result = await priority_service.get_priorities()
        
        # Assert
        assert isinstance(result, responses.GetPriorities)
        assert len(result.items) == 0
    
    async def test_create_priority_success(self, priority_service, mock_priority_repository, mock_priority_model):
        """Test successful priority creation."""
        # Arrange
        create_params = params.CreatePriority(
            name="Critical",
            description="Critical priority"
        )
        mock_priority_repository.new = AsyncMock(return_value=mock_priority_model)
        
        # Act
        result = await priority_service.create_priority(create_params)
        
        # Assert
        assert isinstance(result, responses.Priority)
        mock_priority_repository.new.assert_called_once()
    
    async def test_create_priority_failure(self, priority_service, mock_priority_repository):
        """Test priority creation failure."""
        # Arrange
        create_params = params.CreatePriority(
            name="Critical",
            description="Critical priority"
        )
        mock_priority_repository.new = AsyncMock(return_value=None)
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await priority_service.create_priority(create_params)
        
        assert exc_info.value.status_code == 500
    
    async def test_delete_priority_success(self, priority_service, mock_priority_repository, mock_priority_model):
        """Test successful priority deletion."""
        # Arrange
        priority_id = 1
        mock_priority_repository.get_by_id = AsyncMock(return_value=mock_priority_model)
        mock_priority_repository.delete = AsyncMock(return_value=True)
        
        # Act
        result = await priority_service.delete_priority(priority_id)
        
        # Assert
        assert isinstance(result, responses.Priority)
        mock_priority_repository.delete.assert_called_once()
    
    async def test_delete_priority_not_found(self, priority_service, mock_priority_repository):
        """Test priority deletion when priority doesn't exist."""
        # Arrange
        priority_id = 999
        mock_priority_repository.get_by_id = AsyncMock(return_value=None)
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await priority_service.delete_priority(priority_id)
        
        assert exc_info.value.status_code == 404
    
    async def test_update_priority_success(self, priority_service, mock_priority_repository, mock_priority_model):
        """Test successful priority update."""
        # Arrange
        priority_id = 1
        update_params = params.UpdatePriority(
            name="Updated Priority",
            description="Updated description"
        )
        
        updated_model = MagicMock(spec=Priority)
        updated_model.id = priority_id
        updated_model.name = "Updated Priority"
        
        mock_priority_repository.get_by_id = AsyncMock(return_value=mock_priority_model)
        mock_priority_repository.update = AsyncMock(return_value=updated_model)
        
        # Act
        result = await priority_service.update_priority(update_params, priority_id)
        
        # Assert
        assert isinstance(result, responses.Priority)
        mock_priority_repository.update.assert_called_once()
    
    async def test_update_priority_not_found(self, priority_service, mock_priority_repository):
        """Test priority update when priority doesn't exist."""
        # Arrange
        priority_id = 999
        update_params = params.UpdatePriority(
            name="Updated Priority"
        )
        mock_priority_repository.get_by_id = AsyncMock(return_value=None)
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await priority_service.update_priority(update_params, priority_id)
        
        assert exc_info.value.status_code == 404
