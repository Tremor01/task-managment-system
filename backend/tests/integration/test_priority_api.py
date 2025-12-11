"""
Integration tests for Priority API endpoints
"""
import pytest
from httpx import AsyncClient
from fastapi import status

@pytest.mark.integration
class TestPriorityAPI:
    """Test Priority API endpoints with real database."""

    async def test_create_priority(self, async_client: AsyncClient, sample_priority_data: dict):
        """Test creating a priority via API."""
        # Act
        response = await async_client.post("/api/priorities/", json=sample_priority_data)

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["name"] == sample_priority_data["name"]
        assert data["description"] == sample_priority_data["description"]
        assert "id" in data

    async def test_get_priorities(self, async_client: AsyncClient, test_priority: dict):
        """Test getting all priorities via API."""
        # Act
        response = await async_client.get("/api/priorities/")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data["items"], list)
        assert len(data["items"]) >= 1
        assert any(priority["id"] == test_priority.id for priority in data["items"])

    async def test_get_priority_by_id(self, async_client: AsyncClient, test_priority: dict):
        """Test getting a specific priority by ID."""
        # Act
        response = await async_client.get(f"/api/priorities/{test_priority.id}")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == test_priority.id
        assert data["name"] == test_priority.name

    async def test_update_priority(self, async_client: AsyncClient, test_priority: dict):
        """Test updating a priority via API."""
        # Arrange
        update_data = {
            "name": "Updated Priority",
            "description": "Updated description"
        }

        # Act
        response = await async_client.put(f"/api/priorities/{test_priority.id}", json=update_data)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == test_priority.id
        assert data["name"] == update_data["name"]
        assert data["description"] == update_data["description"]

    async def test_delete_priority(self, async_client: AsyncClient, test_priority: dict):
        """Test deleting a priority via API."""
        # Act
        response = await async_client.delete(f"/api/priorities/{test_priority.id}")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == test_priority.id

        # Verify deletion
        response = await async_client.get(f"/api/priorities/{test_priority.id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_get_nonexistent_priority(self, async_client: AsyncClient):
        """Test getting a non-existent priority."""
        # Act
        response = await async_client.get("/api/priorities/999")

        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_delete_nonexistent_priority(self, async_client: AsyncClient):
        """Test deleting a non-existent priority."""
        # Act
        response = await async_client.delete("/api/priorities/999")

        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_update_nonexistent_priority(self, async_client: AsyncClient):
        """Test updating a non-existent priority."""
        # Arrange
        update_data = {
            "name": "Updated Priority",
            "description": "Updated description"
        }

        # Act
        response = await async_client.put("/api/priorities/999", json=update_data)

        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND
