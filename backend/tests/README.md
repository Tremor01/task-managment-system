# Task Management System - Test Suite

This directory contains comprehensive tests for the Task Management System using pytest.

## Test Structure

```
tests/
├── unit/                  # Unit tests (isolated, fast)
├── integration/           # Integration tests (with database)
├── system/                # System/E2E tests (complete workflows)
├── load/                  # Load/performance tests
│   ├── locustfile.py      # Locust load testing
│   └── test_load_performance.py  # pytest-benchmark tests
├── conftest.py            # Global pytest fixtures
└── README.md              # This file
```

## Test Types

### 1. Unit Tests

**Location:** `tests/unit/`

**Purpose:** Test individual components in isolation using mocked dependencies.

**Files:**
- `test_priority_service.py` - Tests for PriorityService
- `test_task_service.py` - Tests for TaskService
- `test_status_service.py` - Tests for StatusService
- `test_label_service.py` - Tests for LabelService

**Run unit tests:**
```bash
pytest tests/unit/ -m unit
```

### 2. Integration Tests

**Location:** `tests/integration/`

**Purpose:** Test API endpoints with real database interactions.

**Files:**
- `test_priority_api.py` - Tests for Priority API endpoints
- `test_task_api.py` - Tests for Task API endpoints

**Run integration tests:**
```bash
pytest tests/integration/ -m integration
```

### 3. System Tests

**Location:** `tests/system/`

**Purpose:** Test complete workflows and end-to-end scenarios.

**Files:**
- `test_task_workflow.py` - Complete task management workflow tests

**Run system tests:**
```bash
pytest tests/system/ -m system
```

### 4. Load Tests

**Location:** `tests/load/`

**Purpose:** Test system performance under load.

**Files:**
- `locustfile.py` - Locust load testing scenarios
- `test_load_performance.py` - pytest-benchmark performance tests

**Run performance tests:**
```bash
pytest tests/load/ -m load
```

**Run Locust load tests:**
```bash
locust -f tests/load/locustfile.py
```

## Running All Tests

To run all tests:
```bash
pytest tests/
```

To run tests with coverage:
```bash
pytest tests/ --cov=source --cov-report=html
```

## Test Markers

The test suite uses the following pytest markers:

- `@pytest.mark.unit` - Unit tests (fast, isolated)
- `@pytest.mark.integration` - Integration tests (with database)
- `@pytest.mark.system` - System/E2E tests (full workflows)
- `@pytest.mark.load` - Load/Performance tests
- `@pytest.mark.slow` - Tests that take a long time

## Test Fixtures

Global fixtures are defined in `conftest.py`:

- `test_db` - Test database setup/teardown
- `test_session` - Test database session
- `async_client` - Async HTTP client for API testing
- `sample_*_data` - Sample data for testing
- `test_*` - Test entities (priority, status, label, task)
- `mock_*_repository` - Mock repositories for unit tests

## Test Environment

The tests use a separate test database configured in `.env.test` and `docker-compose.test.yml`.

## Best Practices

1. **Unit tests** should be fast and isolated
2. **Integration tests** should test API endpoints with real database
3. **System tests** should test complete user workflows
4. **Load tests** should test performance under realistic conditions
5. Use appropriate markers for each test type
6. Keep tests independent and repeatable
7. Use fixtures for test data setup and cleanup

## Adding New Tests

When adding new tests:

1. Place them in the appropriate directory based on test type
2. Use the appropriate pytest marker
3. Follow the existing patterns and conventions
4. Add any new fixtures to `conftest.py` if needed
5. Ensure tests are independent and can run in any order
