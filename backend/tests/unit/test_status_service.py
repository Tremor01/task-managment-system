"""
Unit tests for StatusService
"""
import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException

from services.status import StatusService
from schemas.status import params, responses
from db.models import Status

@pytest.mark.unit
class TestStatusService:
    """Test StatusService methods in isolation with mocked repositories."""

    @pytest.fixture
    def status_service(self, mock_status_repository):
        """Create StatusService instance with mocked repository."""
        return StatusService(status_repo=mock_status_repository)

    @pytest.fixture
    def mock_status_model(self):
        """Create a mock Status model."""
        status = MagicMock(spec=Status)
        status.id = 1
        status.name = "In Progress"
        status.description = "Tasks currently being worked on"
        return status

    async def test_get_statuses_success(self, status_service, mock_status_repository, mock_status_model):
        """Test successful retrieval of statuses."""
        # Arrange
        mock_status_repository.select_all = AsyncMock(return_value=[mock_status_model])

        # Act
        result = await status_service.get_statuses()

        # Assert
        assert isinstance(result, responses.GetStatuses)
        assert len(result.items) == 1
        mock_status_repository.select_all.assert_called_once()

    async def test_get_statuses_empty(self, status_service, mock_status_repository):
        """Test get_statuses when no statuses exist."""
        # Arrange
        mock_status_repository.select_all = AsyncMock(return_value=[])

        # Act
        result = await status_service.get_statuses()

        # Assert
        assert isinstance(result, responses.GetStatuses)
        assert len(result.items) == 0

    async def test_create_status_success(self, status_service, mock_status_repository, mock_status_model):
        """Test successful status creation."""
        # Arrange
        create_params = params.CreateStatus(
            name="Completed",
            description="Tasks that are completed"
        )
        mock_status_repository.new = AsyncMock(return_value=mock_status_model)

        # Act
        result = await status_service.create_status(create_params)

        # Assert
        assert isinstance(result, responses.Status)
        mock_status_repository.new.assert_called_once()

    async def test_create_status_failure(self, status_service, mock_status_repository):
        """Test status creation failure."""
        # Arrange
        create_params = params.CreateStatus(
            name="Completed",
            description="Tasks that are completed"
        )
        mock_status_repository.new = AsyncMock(return_value=None)

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await status_service.create_status(create_params)

        assert exc_info.value.status_code == 500

    async def test_delete_status_success(self, status_service, mock_status_repository, mock_status_model):
        """Test successful status deletion."""
        # Arrange
        status_id = 1
        mock_status_repository.get_by_id = AsyncMock(return_value=mock_status_model)
        mock_status_repository.delete = AsyncMock(return_value=True)

        # Act
        result = await status_service.delete_status(status_id)

        # Assert
        assert isinstance(result, responses.Status)
        mock_status_repository.delete.assert_called_once()

    async def test_delete_status_not_found(self, status_service, mock_status_repository):
        """Test status deletion when status doesn't exist."""
        # Arrange
        status_id = 999
        mock_status_repository.get_by_id = AsyncMock(return_value=None)

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await status_service.delete_status(status_id)

        assert exc_info.value.status_code == 404

    async def test_update_status_success(self, status_service, mock_status_repository, mock_status_model):
        """Test successful status update."""
        # Arrange
        status_id = 1
        update_params = params.UpdateStatus(
            name="Updated Status",
            description="Updated description"
        )

        updated_model = MagicMock(spec=Status)
        updated_model.id = status_id
        updated_model.name = "Updated Status"

        mock_status_repository.get_by_id = AsyncMock(return_value=mock_status_model)
        mock_status_repository.update = AsyncMock(return_value=updated_model)

        # Act
        result = await status_service.update_status(update_params, status_id)

        # Assert
        assert isinstance(result, responses.Status)
        mock_status_repository.update.assert_called_once()

    async def test_update_status_not_found(self, status_service, mock_status_repository):
        """Test status update when status doesn't exist."""
        # Arrange
        status_id = 999
        update_params = params.UpdateStatus(
            name="Updated Status"
        )
        mock_status_repository.get_by_id = AsyncMock(return_value=None)

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await status_service.update_status(update_params, status_id)

        assert exc_info.value.status_code == 404
