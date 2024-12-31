import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from routes.v1.stories import router
from models.story import Story
from models.event import Event

# Crear una instancia de FastAPI para pruebas
app = FastAPI()
app.include_router(router)

# Usar TestClient para las pruebas
client = TestClient(app)


def test_get_stories_endpoint():
    """Prueba el endpoint GET /v1/stories."""
    response = client.get("/v1/stories")
    assert response.status_code == 200

    # Verificar que la respuesta tiene la clave 'stories'
    data = response.json()
    assert "stories" in data
    assert isinstance(data["stories"], list)

    # Validar que cada elemento en la lista es un Story válido
    for item in data["stories"]:
        story = Story(**item)  
        assert isinstance(story, Story)

def test_post_stories_endpoint():
    """Prueba el endpoint POST /v1/stories."""
    new_events = [
        {
            "event": "user_click",
            "properties": {
                "distinct_id": "12345",
                "session_id": "abc",
                "journey_id": "xyz",
                "$current_url": "https://example.com",
                "$host": "example.com",
                "$pathname": "/test",
                "$browser": "Chrome",
                "$device": "Desktop",
                "$screen_height": 1080,
                "$screen_width": 1920,
                "eventType": "click",
                "elementType": "button",
                "elementText": "Submit",
                "elementAttributes": {
                    "class": "btn-primary",
                    "href": "/submit"
                },
                "timestamp": "2024-01-01T00:00:00Z",
                "x": 100,
                "y": 200,
                "mouseButton": 0,
                "ctrlKey": False,
                "shiftKey": False,
                "altKey": False,
                "metaKey": False
            },
            "timestamp": "2024-01-01T00:00:00Z"
        }
    ]

    response = client.post("/v1/stories", json=new_events)
    assert response.status_code == 200
    assert response.json()["message"] == "Stories created or updated successfully."



def test_get_patterns_endpoint():
    """Prueba el endpoint GET /v1/stories/patterns."""
    response = client.get("/v1/stories/patterns")
    assert response.status_code == 200

    # Verificar que la respuesta es un diccionario
    data = response.json()
    assert isinstance(data, dict)

    # Verificar que las claves son los nombres esperados de patrones
    expected_keys = [
        "ambiguous_interaction",
        "interaction_with_highlighted_content",
        "repeated_click"
    ]
    for key in expected_keys:
        assert key in data

    # Verificar que los valores son diccionarios con historias
    for key, value in data.items():
        assert isinstance(value, dict)
        for story_id, count in value.items():
            assert isinstance(story_id, str)  # Verificar que las claves son IDs de historias
            assert isinstance(count, int)    # Verificar que los valores son enteros



