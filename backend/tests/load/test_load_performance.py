"""
Performance tests using pytest-benchmark
"""
import pytest
import asyncio
from httpx import AsyncClient
from fastapi import status
import random
import string
from datetime import datetime, timedelta

@pytest.mark.load
@pytest.mark.slow
class TestPerformance:
    """Performance tests for the task management system."""

    def _generate_random_string(self, length=10):
        """Generate random string for test data."""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    async def _setup_test_data(self, async_client: AsyncClient):
        """Setup test data for performance tests."""
        # Create priority
        priority_data = {"name": self._generate_random_string(), "description": "Test priority"}
        priority_response = await async_client.post("/api/priorities/", json=priority_data)
        priority_id = priority_response.json()["id"]

        # Create status
        status_data = {"name": self._generate_random_string(), "description": "Test status"}
        status_response = await async_client.post("/api/statuses/", json=status_data)
        status_id = status_response.json()["id"]

        # Create label
        label_data = {"name": self._generate_random_string(), "description": "Test label"}
        label_response = await async_client.post("/api/labels/", json=label_data)
        label_id = label_response.json()["id"]

        return priority_id, status_id, label_id

    @pytest.mark.benchmark(group="create-tasks")
    async def test_create_many_tasks_performance(self, async_client: AsyncClient, benchmark):
        """Test performance of creating many tasks."""
        priority_id, status_id, label_id = await self._setup_test_data(async_client)

        # Benchmark creating 100 tasks
        def create_tasks():
            tasks = []
            for i in range(100):
                task_data = {
                    "description": f"Performance test task {i}",
                    "deadline": (datetime.now() + timedelta(days=30)).isoformat(),
                    "priority_id": priority_id,
                    "status_id": status_id,
                    "label_id": label_id
                }
                tasks.append(async_client.post("/api/tasks/", json=task_data))
            return asyncio.gather(*tasks)

        # Run the benchmark
        results = await benchmark(create_tasks)

        # Verify all tasks were created successfully
        for result in results:
            assert result.status_code == status.HTTP_201_CREATED

    @pytest.mark.benchmark(group="read-tasks")
    async def test_get_all_tasks_performance(self, async_client: AsyncClient, benchmark):
        """Test performance of getting all tasks."""
        # First create some tasks for the benchmark
        priority_id, status_id, label_id = await self._setup_test_data(async_client)

        # Create 50 tasks
        for i in range(50):
            task_data = {
                "description": f"Performance test task {i}",
                "deadline": (datetime.now() + timedelta(days=30)).isoformat(),
                "priority_id": priority_id,
                "status_id": status_id,
                "label_id": label_id
            }
            await async_client.post("/api/tasks/", json=task_data)

        # Benchmark getting all tasks
        def get_tasks():
            return async_client.get("/api/tasks/")

        # Run the benchmark
        response = await benchmark(get_tasks)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["items"]) >= 50

    @pytest.mark.benchmark(group="update-tasks")
    async def test_update_many_tasks_performance(self, async_client: AsyncClient, benchmark):
        """Test performance of updating many tasks."""
        priority_id, status_id, label_id = await self._setup_test_data(async_client)

        # Create a new status for updates
        new_status_data = {"name": self._generate_random_string(), "description": "New status"}
        new_status_response = await async_client.post("/api/statuses/", json=new_status_data)
        new_status_id = new_status_response.json()["id"]

        # Create 20 tasks to update
        task_ids = []
        for i in range(20):
            task_data = {
                "description": f"Performance test task {i}",
                "deadline": (datetime.now() + timedelta(days=30)).isoformat(),
                "priority_id": priority_id,
                "status_id": status_id,
                "label_id": label_id
            }
            response = await async_client.post("/api/tasks/", json=task_data)
            task_ids.append(response.json()["id"])

        # Benchmark updating all tasks
        def update_tasks():
            updates = []
            for task_id in task_ids:
                update_data = {
                    "description": f"Updated performance test task {task_id}",
                    "status_id": new_status_id
                }
                updates.append(async_client.put(f"/api/tasks/{task_id}", json=update_data))
            return asyncio.gather(*updates)

        # Run the benchmark
        results = await benchmark(update_tasks)

        # Verify all updates were successful
        for result in results:
            assert result.status_code == status.HTTP_200_OK

    @pytest.mark.benchmark(group="delete-tasks")
    async def test_delete_many_tasks_performance(self, async_client: AsyncClient, benchmark):
        """Test performance of deleting many tasks."""
        priority_id, status_id, label_id = await self._setup_test_data(async_client)

        # Create 30 tasks to delete
        task_ids = []
        for i in range(30):
            task_data = {
                "description": f"Performance test task {i}",
                "deadline": (datetime.now() + timedelta(days=30)).isoformat(),
                "priority_id": priority_id,
                "status_id": status_id,
                "label_id": label_id
            }
            response = await async_client.post("/api/tasks/", json=task_data)
            task_ids.append(response.json()["id"])

        # Benchmark deleting all tasks
        def delete_tasks():
            deletes = []
            for task_id in task_ids:
                deletes.append(async_client.delete(f"/api/tasks/{task_id}"))
            return asyncio.gather(*deletes)

        # Run the benchmark
        results = await benchmark(delete_tasks)

        # Verify all deletions were successful
        for result in results:
            assert result.status_code == status.HTTP_200_OK

    @pytest.mark.benchmark(group="filter-tasks")
    async def test_filter_tasks_performance(self, async_client: AsyncClient, benchmark):
        """Test performance of filtering tasks."""
        priority_id, status_id, label_id = await self._setup_test_data(async_client)

        # Create 100 tasks with different priorities and statuses
        for i in range(100):
            task_data = {
                "description": f"Performance test task {i}",
                "deadline": (datetime.now() + timedelta(days=30)).isoformat(),
                "priority_id": priority_id,
                "status_id": status_id,
                "label_id": label_id
            }
            await async_client.post("/api/tasks/", json=task_data)

        # Benchmark filtering tasks by priority
        def filter_tasks():
            return async_client.get(f"/api/tasks/?priority_id={priority_id}")

        # Run the benchmark
        response = await benchmark(filter_tasks)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["items"]) >= 100
