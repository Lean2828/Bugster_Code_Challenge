import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock
from main import app
from dependencies import get_database_manager

@pytest.fixture
def test_client():
    """
    Fixture para crear un cliente de pruebas.
    """
    return TestClient(app)

@pytest.fixture
def mock_db_manager():
    """
    Fixture para mockear el DatabaseManager.
    """
    mock = AsyncMock()
    # Configuración por defecto de los métodos mockeados
    mock.get_all_stories.return_value = []
    mock.get_stories_by_session_id.return_value = []
    mock.get_stories_by_story_id.return_value = []
    mock.bulk_upsert_stories.return_value = None
    return mock

@pytest.fixture(autouse=True)
def override_dependencies(mock_db_manager):
    """
    Fixture para sobrescribir las dependencias en FastAPI con el mock del DatabaseManager.
    """
    app.dependency_overrides[get_database_manager] = lambda: mock_db_manager
    yield
    app.dependency_overrides = {}  # Limpia los overrides al finalizar el test
