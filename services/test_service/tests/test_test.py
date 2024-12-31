from fastapi import FastAPI
import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock
from routes.v1.tests import router as router

app = FastAPI()
app.include_router(router)

# Usar TestClient para las pruebas
client = TestClient(app)

@pytest.fixture
def mock_database_manager(mocker):
    # Crear un mock para `DatabaseManager`
    mock_db_manager = MagicMock()
    mock_db_manager.get_stories_by_session_id = AsyncMock(return_value=[
        {
            "id": "story-1",
            "session_id": "session-1",
            "title": "Mock Story",
            "startTimestamp": "2024-01-01T00:00:00Z",
            "endTimestamp": "2024-01-01T01:00:00Z",
            "initialState": {"url": "https://example.com"},
            "finalState": {"url": "https://example.com/final"},
            "actions": [{"type": "click", "target": "button", "value": "Submit"}],
            "networkRequests": []
        }
    ])
    mocker.patch(
        "dependencies.get_database_manager",
        return_value=mock_db_manager
    )
    return mock_db_manager

def test_get_tests_endpoint(mocker):
    # Mock para `fetch_stories`
    mock_fetch_stories = mocker.patch(
        "test_application.fetch_stories",
        return_value=[
            {
                "id": "story-1",
                "session_id": "session-1",
                "title": "Mock Story",
                "startTimestamp": "2024-01-01T00:00:00Z",
                "endTimestamp": "2024-01-01T01:00:00Z",
                "initialState": {"url": "https://example.com"},
                "finalState": {"url": "https://example.com/final"},
                "actions": [{"type": "click", "target": "button", "value": "Submit"}],
                "networkRequests": []
            }
        ]
    )

    # Crear un cliente de pruebas
    with TestClient(app) as client:
        response = client.get("/v1/tests/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["story_id"] == "story-1"
