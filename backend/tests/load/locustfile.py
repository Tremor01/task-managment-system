"""
Load tests for Task Management System using Locust
"""
from locust import HttpUser, task, between
from random import choice, randint
from datetime import datetime, timedelta
import uuid

class TaskManagementUser(HttpUser):
    """User behavior for task management system load testing."""
    wait_time = between(1, 5)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Generate some test data
        self.priorities = [
            {"name": "High", "description": "High priority tasks"},
            {"name": "Medium", "description": "Medium priority tasks"},
            {"name": "Low", "description": "Low priority tasks"}
        ]

        self.statuses = [
            {"name": "To Do", "description": "Tasks to be done"},
            {"name": "In Progress", "description": "Tasks being worked on"},
            {"name": "Completed", "description": "Completed tasks"}
        ]

        self.labels = [
            {"name": "Bug", "description": "Bug-related tasks"},
            {"name": "Feature", "description": "Feature-related tasks"},
            {"name": "Refactoring", "description": "Code refactoring tasks"}
        ]

        self.created_priorities = {}
        self.created_statuses = {}
        self.created_labels = {}
        self.created_tasks = {}

    def on_start(self):
        """Setup test data when user starts."""
        # Create priorities
        for priority in self.priorities:
            response = self.client.post("/api/priorities/", json=priority)
            if response.status_code == 201:
                data = response.json()
                self.created_priorities[priority["name"]] = data["id"]

        # Create statuses
        for status in self.statuses:
            response = self.client.post("/api/statuses/", json=status)
            if response.status_code == 201:
                data = response.json()
                self.created_statuses[status["name"]] = data["id"]

        # Create labels
        for label in self.labels:
            response = self.client.post("/api/labels/", json=label)
            if response.status_code == 201:
                data = response.json()
                self.created_labels[label["name"]] = data["id"]

    @task(3)
    def create_task(self):
        """Create a new task."""
        if self.created_priorities and self.created_statuses and self.created_labels:
            priority_id = choice(list(self.created_priorities.values()))
            status_id = choice(list(self.created_statuses.values()))
            label_id = choice(list(self.created_labels.values()))

            task_data = {
                "description": f"Task {uuid.uuid4().hex[:8]}",
                "deadline": (datetime.now() + timedelta(days=randint(1, 30))).isoformat(),
                "priority_id": priority_id,
                "status_id": status_id,
                "label_id": label_id
            }

            response = self.client.post("/api/tasks/", json=task_data)
            if response.status_code == 201:
                data = response.json()
                self.created_tasks[data["id"]] = True

    @task(5)
    def get_tasks(self):
        """Get all tasks."""
        self.client.get("/api/tasks/")

    @task(2)
    def get_task_by_id(self):
        """Get a specific task by ID."""
        if self.created_tasks:
            task_id = choice(list(self.created_tasks.keys()))
            self.client.get(f"/api/tasks/{task_id}")

    @task(1)
    def update_task(self):
        """Update a task."""
        if self.created_tasks:
            task_id = choice(list(self.created_tasks.keys()))
            update_data = {
                "description": f"Updated task {uuid.uuid4().hex[:8]}",
                "status_id": choice(list(self.created_statuses.values()))
            }
            self.client.put(f"/api/tasks/{task_id}", json=update_data)

    @task(1)
    def delete_task(self):
        """Delete a task."""
        if self.created_tasks:
            task_id = choice(list(self.created_tasks.keys()))
            response = self.client.delete(f"/api/tasks/{task_id}")
            if response.status_code == 200:
                del self.created_tasks[task_id]

    @task(2)
    def get_priorities(self):
        """Get all priorities."""
        self.client.get("/api/priorities/")

    @task(1)
    def get_statuses(self):
        """Get all statuses."""
        self.client.get("/api/statuses/")

    @task(1)
    def get_labels(self):
        """Get all labels."""
        self.client.get("/api/labels/")

    @task(1)
    def filter_tasks_by_status(self):
        """Filter tasks by status."""
        if self.created_statuses:
            status_id = choice(list(self.created_statuses.values()))
            self.client.get(f"/api/tasks/?status_id={status_id}")

    @task(1)
    def filter_tasks_by_priority(self):
        """Filter tasks by priority."""
        if self.created_priorities:
            priority_id = choice(list(self.created_priorities.values()))
            self.client.get(f"/api/tasks/?priority_id={priority_id}")

class HeavyTaskUser(HttpUser):
    """Heavy user that creates and manages many tasks."""
    wait_time = between(0.5, 2)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.created_tasks = set()

    def on_start(self):
        """Setup initial data."""
        # Create a priority, status, and label for this user
        priority_response = self.client.post("/api/priorities/", json={
            "name": f"Priority {uuid.uuid4().hex[:4]}",
            "description": "Test priority"
        })
        if priority_response.status_code == 201:
            self.priority_id = priority_response.json()["id"]

        status_response = self.client.post("/api/statuses/", json={
            "name": f"Status {uuid.uuid4().hex[:4]}",
            "description": "Test status"
        })
        if status_response.status_code == 201:
            self.status_id = status_response.json()["id"]

        label_response = self.client.post("/api/labels/", json={
            "name": f"Label {uuid.uuid4().hex[:4]}",
            "description": "Test label"
        })
        if label_response.status_code == 201:
            self.label_id = label_response.json()["id"]

    @task
    def create_many_tasks(self):
        """Create multiple tasks in one go."""
        if hasattr(self, 'priority_id') and hasattr(self, 'status_id') and hasattr(self, 'label_id'):
            for i in range(5):  # Create 5 tasks per call
                task_data = {
                    "description": f"Bulk task {uuid.uuid4().hex[:8]}",
                    "deadline": (datetime.now() + timedelta(days=randint(1, 30))).isoformat(),
                    "priority_id": self.priority_id,
                    "status_id": self.status_id,
                    "label_id": self.label_id
                }
                response = self.client.post("/api/tasks/", json=task_data)
                if response.status_code == 201:
                    self.created_tasks.add(response.json()["id"])

    @task
    def get_all_tasks(self):
        """Get all tasks (heavy read operation)."""
        self.client.get("/api/tasks/")

    @task
    def cleanup_tasks(self):
        """Clean up created tasks."""
        if self.created_tasks:
            task_id = self.created_tasks.pop()
            self.client.delete(f"/api/tasks/{task_id}")
