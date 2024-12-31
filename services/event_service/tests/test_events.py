import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from fastapi import FastAPI
from routes.v1.events import router
from models.event import Event

app = FastAPI()
app.include_router(router)

client = TestClient(app)

@pytest.fixture
def mock_db_manager(mocker):
    """
    Mock para DatabaseManager.
    """
    mock_db_manager = mocker.patch("dependencies.get_database_manager")
    mock_db_manager.return_value.bulk_save_events = mocker.MagicMock()
    mock_db_manager.return_value.bulk_upsert_sessions = mocker.MagicMock()
    return mock_db_manager


@pytest.fixture
def mock_notify_stories_service(mocker):
    """
    Mock para notify_stories_service.
    """
    with patch("event_application.notify_stories_service", new=AsyncMock()) as mock_service:
        yield mock_service

def test_process_events_success(mock_db_manager, mock_notify_stories_service):
    """
    Prueba el procesamiento exitoso de eventos.
    """
    mock_notify_stories_service.return_value = None  

    events = [
        {
            "event": "Test Event",
            "properties": {
                "distinct_id": "user-123",
                "session_id": "session-456",
                "$current_url": "https://example.com/page",
                "$host": "example.com",
                "$pathname": "/page",
                "$browser": "Chrome",
                "$device": "Desktop",
                "$screen_height": 1080,
                "$screen_width": 1920,
                "eventType": "click",
                "elementType": "button",
                "elementText": "Submit",
                "timestamp": "2024-12-30T00:00:00Z",
                "x": 100,
                "y": 200,
                "mouseButton": 0,
                "ctrlKey": False,
                "shiftKey": False,
                "altKey": False,
                "metaKey": False,
            },
            "timestamp": "2024-12-30T00:00:00Z"
        }
    ]

    response = client.post("/v1/events/", json=events)

    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["message"] == f"{len(events)} eventos procesados correctamente."

