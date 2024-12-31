import httpx
import os
from dotenv import load_dotenv
from typing import List, Optional
from models.story import Story
from models.test import Test
from database_manager import DatabaseManager
from logging_config import logger

load_dotenv()
STORIES_SERVICE_URL = os.getenv("STORIES_SERVICE_URL")

async def fetch_stories(story_id: Optional[str] = None) -> List[Story]:
    """
    Recupera historias desde el servicio de historias mediante su endpoint.

    Args:
        story_id (Optional[str]): Identificador único de la historia (opcional).

    Returns:
        List[Story]: Lista de historias instanciadas.
    """
    if not STORIES_SERVICE_URL:
        raise Exception("STORIES_SERVICE_URL no configurado en las variables de entorno.")
    
    try:
        url = f"{STORIES_SERVICE_URL}?story_id={story_id}" if story_id else STORIES_SERVICE_URL
        logger.info(f"Solicitando historias al servicio de historias: {url}")

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()

        stories_data = response.json()

        if not isinstance(stories_data, dict) or 'stories' not in stories_data:
            logger.error(f"El formato de la respuesta no es válido: {stories_data}")
            raise Exception("El formato de la respuesta no es válido: se esperaba un diccionario con la clave 'stories'.")

        stories_list = stories_data.get('stories', [])

        if not isinstance(stories_list, list):
            logger.error(f"El formato de la lista de historias no es válido: {stories_list}")
            raise Exception("El formato de la lista de historias no es válido: se esperaba una lista.")

        valid_stories = []
        for story_data in stories_list:
            if isinstance(story_data, dict):
                try:
                    valid_stories.append(Story(**story_data))
                except Exception as e:
                    logger.warning(f"Historia inválida: {story_data}. Error: {str(e)}")
            else:
                logger.warning(f"Elemento no válido en historias: {story_data}")

        logger.info(f"Se recuperaron {len(valid_stories)} historias válidas del servicio.")
        return valid_stories

    except httpx.HTTPError as e:
        logger.error(f"Error al recuperar historias desde el servicio: {e}", exc_info=True)
        raise Exception(f"Error al obtener historias: {str(e)}")


async def generate_tests(db_manager: DatabaseManager, story_id: Optional[str] = None) -> List[Test]:
    """
    Genera tests de Playwright basados en historias de usuario.

    Args:
        db_manager (DatabaseManager): Gestor de base de datos.
        story_id (Optional[str]): Identificador único de la historia (opcional).

    Returns:
        List[Test]: Lista de tests generados.
    """
    try:
        stories = await fetch_stories(story_id)
        if not stories:
            logger.warning(f"No se encontraron historias para story_id={story_id}")
            return []

        valid_stories = [
            Story(**story) if isinstance(story, dict) else story
            for story in stories
        ]
        
        logger.info(f"Generando tests para {len(valid_stories)} historias...")
        tests = [Test.from_story(story) for story in valid_stories]
        logger.info(f"Se generaron {len(tests)} tests exitosamente.")
        return tests

    except Exception as e:
        logger.error(f"Error generando tests: {e}", exc_info=True)
        raise Exception(f"Error generando tests: {str(e)}")
