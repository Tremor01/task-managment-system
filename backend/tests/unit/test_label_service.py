"""
Unit tests for LabelService
"""
import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException

from source.services.label import LabelService
from source.schemas.label import params, responses
from source.db.models import Label

@pytest.mark.unit
class TestLabelService:
    """Test LabelService methods in isolation with mocked repositories."""

    @pytest.fixture
    def label_service(self, mock_label_repository):
        """Create LabelService instance with mocked repository."""
        return LabelService(label_repo=mock_label_repository)

    @pytest.fixture
    def mock_label_model(self):
        """Create a mock Label model."""
        label = MagicMock(spec=Label)
        label.id = 1
        label.name = "Bug"
        label.description = "Bug-related tasks"
        return label

    async def test_get_labels_success(self, label_service, mock_label_repository, mock_label_model):
        """Test successful retrieval of labels."""
        # Arrange
        mock_label_repository.select_all = AsyncMock(return_value=[mock_label_model])

        # Act
        result = await label_service.get_labels(params.GetLabels())

        # Assert
        assert isinstance(result, responses.GetLabels)
        assert len(result.items) == 1
        mock_label_repository.select_all.assert_called_once()

    async def test_get_labels_empty(self, label_service, mock_label_repository):
        """Test get_labels when no labels exist."""
        # Arrange
        mock_label_repository.select_all = AsyncMock(return_value=[])

        # Act
        result = await label_service.get_labels(params.GetLabels())

        # Assert
        assert isinstance(result, responses.GetLabels)
        assert len(result.items) == 0

    async def test_create_label_success(self, label_service, mock_label_repository, mock_label_model):
        """Test successful label creation."""
        # Arrange
        create_params = params.CreateLabel(
            name="Feature",
            description="Feature-related tasks"
        )
        mock_label_repository.new = AsyncMock(return_value=mock_label_model)

        # Act
        result = await label_service.create_label(create_params)

        # Assert
        assert isinstance(result, responses.Label)
        mock_label_repository.new.assert_called_once()

    async def test_create_label_failure(self, label_service, mock_label_repository):
        """Test label creation failure."""
        # Arrange
        create_params = params.CreateLabel(
            name="Feature",
            description="Feature-related tasks"
        )
        mock_label_repository.new = AsyncMock(return_value=None)

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await label_service.create_label(create_params)

        assert exc_info.value.status_code == 500

    async def test_delete_label_success(self, label_service, mock_label_repository, mock_label_model):
        """Test successful label deletion."""
        # Arrange
        label_id = 1
        mock_label_repository.get_by_id = AsyncMock(return_value=mock_label_model)
        mock_label_repository.delete = AsyncMock(return_value=True)

        # Act
        result = await label_service.delete_label(label_id)

        # Assert
        assert isinstance(result, MagicMock)
        mock_label_repository.delete.assert_called_once()

    async def test_delete_label_not_found(self, label_service, mock_label_repository):
        """Test label deletion when label doesn't exist."""
        # Arrange
        label_id = 999
        mock_label_repository.get_by_id = AsyncMock(return_value=None)

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await label_service.delete_label(label_id)

        assert exc_info.value.status_code == 404

    async def test_update_label_success(self, label_service, mock_label_repository, mock_label_model):
        """Test successful label update."""
        # Arrange
        label_id = 1
        update_params = params.UpdateLabel(
            name="Updated Label"
        )

        updated_model = MagicMock(spec=Label)
        updated_model.id = label_id
        updated_model.name = "Updated Label"

        mock_label_repository.get_by_id = AsyncMock(return_value=mock_label_model)
        mock_label_repository.update = AsyncMock(return_value=updated_model)

        # Act
        result = await label_service.update_label(update_params, label_id)

        # Assert
        assert isinstance(result, responses.Label)
        mock_label_repository.update.assert_called_once()

    async def test_update_label_not_found(self, label_service, mock_label_repository):
        """Test label update when label doesn't exist."""
        # Arrange
        label_id = 999
        update_params = params.UpdateLabel(
            name="Updated Label"
        )
        mock_label_repository.get_by_id = AsyncMock(return_value=None)

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await label_service.update_label(update_params, label_id)

        assert exc_info.value.status_code == 404
