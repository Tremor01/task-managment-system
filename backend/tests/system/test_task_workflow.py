"""
System tests for complete task management workflow
"""
import pytest
from httpx import AsyncClient
from fastapi import status

@pytest.mark.system
class TestTaskWorkflow:
    """Test complete task management workflow from creation to completion."""

    async def test_complete_task_workflow(self, async_client: AsyncClient):
        """Test the complete workflow of creating and managing a task."""
        # Step 1: Create priority, status, and label
        priority_data = {"name": "High", "description": "High priority tasks"}
        status_data = {"name": "To Do", "description": "Tasks to be done"}
        label_data = {"name": "Bug", "description": "Bug-related tasks"}

        priority_response = await async_client.post("/api/priorities/", json=priority_data)
        assert priority_response.status_code == status.HTTP_201_CREATED
        priority_id = priority_response.json()["id"]

        status_response = await async_client.post("/api/statuses/", json=status_data)
        assert status_response.status_code == status.HTTP_201_CREATED
        status_id = status_response.json()["id"]

        label_response = await async_client.post("/api/labels/", json=label_data)
        assert label_response.status_code == status.HTTP_201_CREATED
        label_id = label_response.json()["id"]

        # Step 2: Create a task
        task_data = {
            "description": "Fix critical bug in authentication",
            "deadline": "2025-12-31T23:59:59",
            "priority_id": priority_id,
            "status_id": status_id,
            "label_id": label_id
        }

        task_response = await async_client.post("/api/tasks/", json=task_data)
        assert task_response.status_code == status.HTTP_201_CREATED
        task_id = task_response.json()["id"]

        # Step 3: Verify task creation
        get_task_response = await async_client.get(f"/api/tasks/{task_id}")
        assert get_task_response.status_code == status.HTTP_200_OK
        task_data = get_task_response.json()
        assert task_data["description"] == "Fix critical bug in authentication"
        assert task_data["priority_id"] == priority_id
        assert task_data["status_id"] == status_id

        # Step 4: Update task status to "In Progress"
        in_progress_status_data = {"name": "In Progress", "description": "Tasks being worked on"}
        in_progress_response = await async_client.post("/api/statuses/", json=in_progress_status_data)
        in_progress_status_id = in_progress_response.json()["id"]

        update_task_data = {
            "description": "Fix critical bug in authentication - in progress",
            "status_id": in_progress_status_id
        }

        update_response = await async_client.put(f"/api/tasks/{task_id}", json=update_task_data)
        assert update_response.status_code == status.HTTP_200_OK

        # Step 5: Verify task update
        updated_task_response = await async_client.get(f"/api/tasks/{task_id}")
        assert updated_task_response.status_code == status.HTTP_200_OK
        updated_task_data = updated_task_response.json()
        assert updated_task_data["description"] == "Fix critical bug in authentication - in progress"
        assert updated_task_data["status_id"] == in_progress_status_id

        # Step 6: Complete the task
        completed_status_data = {"name": "Completed", "description": "Completed tasks"}
        completed_response = await async_client.post("/api/statuses/", json=completed_status_data)
        completed_status_id = completed_response.json()["id"]

        complete_task_data = {
            "description": "Fix critical bug in authentication - completed",
            "status_id": completed_status_id
        }

        complete_response = await async_client.put(f"/api/tasks/{task_id}", json=complete_task_data)
        assert complete_response.status_code == status.HTTP_200_OK

        # Step 7: Verify task completion
        completed_task_response = await async_client.get(f"/api/tasks/{task_id}")
        assert completed_task_response.status_code == status.HTTP_200_OK
        completed_task_data = completed_task_response.json()
        assert completed_task_data["status_id"] == completed_status_id

        # Step 8: Get all tasks and verify our task is in the list
        all_tasks_response = await async_client.get("/api/tasks/")
        assert all_tasks_response.status_code == status.HTTP_200_OK
        all_tasks_data = all_tasks_response.json()
        assert any(task["id"] == task_id for task in all_tasks_data["items"])

        # Step 9: Filter tasks by status to find completed tasks
        completed_tasks_response = await async_client.get(f"/api/tasks/?status_id={completed_status_id}")
        assert completed_tasks_response.status_code == status.HTTP_200_OK
        completed_tasks_data = completed_tasks_response.json()
        assert any(task["id"] == task_id for task in completed_tasks_data["items"])

        # Step 10: Clean up - delete the task
        delete_response = await async_client.delete(f"/api/tasks/{task_id}")
        assert delete_response.status_code == status.HTTP_200_OK

        # Verify deletion
        deleted_task_response = await async_client.get(f"/api/tasks/{task_id}")
        assert deleted_task_response.status_code == status.HTTP_404_NOT_FOUND

    async def test_task_workflow_with_invalid_data(self, async_client: AsyncClient):
        """Test task workflow with invalid data handling."""
        # Try to create task with invalid priority ID
        task_data = {
            "description": "Invalid task",
            "deadline": "2025-12-31T23:59:59",
            "priority_id": 999,  # Non-existent priority
            "status_id": 999,    # Non-existent status
            "label_id": 999      # Non-existent label
        }

        # This should fail due to foreign key constraints
        response = await async_client.post("/api/tasks/", json=task_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        # Try to get non-existent task
        response = await async_client.get("/api/tasks/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND

        # Try to update non-existent task
        update_data = {"description": "Updated description"}
        response = await async_client.put("/api/tasks/999", json=update_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND

        # Try to delete non-existent task
        response = await async_client.delete("/api/tasks/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
