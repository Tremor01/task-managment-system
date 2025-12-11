"""
Integration tests for Task API endpoints
"""
import pytest
from httpx import AsyncClient
from fastapi import status
from datetime import datetime

@pytest.mark.integration
class TestTaskAPI:
    """Test Task API endpoints with real database."""

    async def test_create_task(self, async_client: AsyncClient, test_priority: dict, test_status: dict, test_label: dict, sample_task_data: dict):
        """Test creating a task via API."""
        # Arrange
        create_data = {
            "description": sample_task_data["description"],
            "deadline": sample_task_data["deadline"],
            "priority_id": test_priority.id,
            "status_id": test_status.id,
            "label_id": test_label.id
        }

        # Act
        response = await async_client.post("/api/tasks/", json=create_data)

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["description"] == create_data["description"]
        assert data["priority_id"] == create_data["priority_id"]
        assert data["status_id"] == create_data["status_id"]
        assert data["label_id"] == create_data["label_id"]
        assert "id" in data

    async def test_get_tasks(self, async_client: AsyncClient, test_task: dict):
        """Test getting all tasks via API."""
        # Act
        response = await async_client.get("/api/tasks/")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data["items"], list)
        assert len(data["items"]) >= 1
        assert any(task["id"] == test_task.id for task in data["items"])

    async def test_get_task_by_id(self, async_client: AsyncClient, test_task: dict):
        """Test getting a specific task by ID."""
        # Act
        response = await async_client.get(f"/api/tasks/{test_task.id}")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == test_task.id
        assert data["description"] == test_task.description

    async def test_update_task(self, async_client: AsyncClient, test_task: dict, test_priority: dict):
        """Test updating a task via API."""
        # Arrange
        update_data = {
            "description": "Updated task description",
            "priority_id": test_priority.id
        }

        # Act
        response = await async_client.put(f"/api/tasks/{test_task.id}", json=update_data)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == test_task.id
        assert data["description"] == update_data["description"]
        assert data["priority_id"] == update_data["priority_id"]

    async def test_delete_task(self, async_client: AsyncClient, test_task: dict):
        """Test deleting a task via API."""
        # Act
        response = await async_client.delete(f"/api/tasks/{test_task.id}")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == test_task.id

        # Verify deletion
        response = await async_client.get(f"/api/tasks/{test_task.id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_get_nonexistent_task(self, async_client: AsyncClient):
        """Test getting a non-existent task."""
        # Act
        response = await async_client.get("/api/tasks/999")

        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_delete_nonexistent_task(self, async_client: AsyncClient):
        """Test deleting a non-existent task."""
        # Act
        response = await async_client.delete("/api/tasks/999")

        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_update_nonexistent_task(self, async_client: AsyncClient):
        """Test updating a non-existent task."""
        # Arrange
        update_data = {
            "description": "Updated task description"
        }

        # Act
        response = await async_client.put("/api/tasks/999", json=update_data)

        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_get_tasks_by_filter(self, async_client: AsyncClient, test_task: dict, test_priority: dict):
        """Test getting tasks filtered by priority."""
        # Act
        response = await async_client.get(f"/api/tasks/?priority_id={test_priority.id}")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data["items"], list)
        assert len(data["items"]) >= 1
        assert all(task["priority_id"] == test_priority.id for task in data["items"])
