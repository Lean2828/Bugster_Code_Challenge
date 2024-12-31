from typing import List, Optional, Dict, Union
from models.story import Story
from models.event import Event
from database_manager import DatabaseManager
from logging_config import logger

async def get_stories(db_manager: DatabaseManager, session_id: Optional[str] = None, story_id: Optional[str] = None) -> List[Story]:
    """
    Recupera historias de la base de datos.

    Args:
        db_manager (DatabaseManager): Gestor de la base de datos.
        session_id (Optional[str]): ID de sesión para filtrar las historias.
        story_id (Optional[str]): ID de la historia para filtrar.

    Returns:
        List[Story]: Lista de historias recuperadas.
    """
    try:
        logger.info(f"Recibiendo parámetros en get_stories_application: session_id={session_id}, story_id={story_id}")

        if session_id:
            logger.info(f"Obteniendo historias por session_id={session_id}")
            stories_data = db_manager.get_stories_by_session_id(session_id)
        elif story_id:
            logger.info(f"Obteniendo historias por story_id={story_id}")
            stories_data = db_manager.get_stories_by_story_id(story_id)
        else:
            logger.info("Obteniendo todas las historias sin filtros")
            stories_data = db_manager.get_all_stories()

        logger.info(f"Historias obtenidas de la base de datos: {len(stories_data)} historias encontradas.")
        stories = [Story(**story_data) for story_data in stories_data]
        return stories

    except Exception as e:
        logger.error(f"Error al obtener historias en get_stories_application: {str(e)}", exc_info=True)
        raise

async def post_stories(events: List[Event], db_manager: DatabaseManager):
    """
    Procesa eventos para agruparlos en historias y las guarda en la base de datos.

    Args:
        events (List[Event]): Lista de eventos proporcionados.
        db_manager (DatabaseManager): Gestor de la base de datos.
    """
    try:
        stories = _group_events_into_stories(events)
        db_manager.bulk_upsert_stories(stories)
    except Exception as e:
        logger.error(f"Error in post_stories: {str(e)}", exc_info=True)
        raise

def _group_events_into_stories(events: List[Event]) -> List[Story]:
    """
    Agrupa eventos por distinct_id y los convierte en historias.

    Args:
        events (List[Event]): Lista de eventos a procesar.

    Returns:
        List[Story]: Historias agrupadas.
    """
    grouped_stories = {}
    for event in events:
        distinct_id = event.properties.distinct_id
        grouped_stories.setdefault(distinct_id, []).append(event)
    
    return [_create_story_from_events(distinct_id, grouped_events) for distinct_id, grouped_events in grouped_stories.items()]

def _create_story_from_events(distinct_id: str, events: List[Event]) -> Story:
    """
    Crea una historia a partir de una lista de eventos.

    Args:
        distinct_id (str): ID único del usuario.
        events (List[Event]): Lista de eventos del usuario.

    Returns:
        Story: Historia generada.
    """
    try:
        events = sorted(events, key=lambda e: e.timestamp)
        return Story(
            id=f"story-{distinct_id}",
            session_id=events[0].properties.session_id,
            title=f"User Story {distinct_id}",
            startTimestamp=events[0].timestamp,
            endTimestamp=events[-1].timestamp,
            initialState={"url": events[0].properties.current_url},
            finalState={"url": events[-1].properties.current_url},
            actions=[
                {
                    "type": event.properties.eventType,
                    "target": event.properties.elementType,
                    "value": event.properties.elementText,
                }
                for event in events
            ],
            networkRequests=[
                event.properties.get("networkRequest")
                for event in events if hasattr(event.properties, "networkRequest")
            ],
        )
    except Exception as e:
        logger.error(f"Error creating story for distinct_id={distinct_id}: {str(e)}", exc_info=True)
        raise

async def get_patterns(db_manager: DatabaseManager, session_id: Optional[str] = None) -> dict:
    """
    Detecta patrones comunes en las historias de usuario.

    Args:
        db_manager (DatabaseManager): Gestor de la base de datos.
        session_id (Optional[str]): ID de sesión para filtrar las historias.

    Returns:
        dict: Diccionario con patrones detectados.
    """
    try:
        stories = await get_stories(db_manager, session_id)
        return _identify_patterns(stories)
    except Exception as e:
        logger.error(f"Error retrieving patterns: {str(e)}", exc_info=True)
        raise

def _identify_patterns(stories: List[Union[Story, dict]]) -> Dict[str, Dict[str, int]]:
    """
    Identifica patrones comunes en las historias proporcionadas.

    Args:
        stories (List[Union[Story, dict]]): Lista de historias como instancias de `Story` o diccionarios.

    Returns:
        Dict[str, Dict[str, int]]: Patrones detectados organizados por tipo.
    """
    patterns = {}

    for story_data in stories:
        if isinstance(story_data, Story):
            story = story_data
        elif isinstance(story_data, dict):
            try:
                story = Story(**story_data)
            except Exception as e:
                logger.warning(f"Error al convertir historia: {story_data}. Error: {str(e)}")
                continue
        else:
            logger.warning(f"Historia no válida encontrada: {story_data}")
            continue

        for action in story.actions:
            # Patrón: Login
            if action.type == "input" and "login" in action.target:
                patterns.setdefault("login", {}).setdefault(story.id, 0)
                patterns["login"][story.id] += 1

            # Patrón: Checkout
            elif action.type == "click" and "checkout" in action.target:
                patterns.setdefault("checkout", {}).setdefault(story.id, 0)
                patterns["checkout"][story.id] += 1

            # Otros patrones
            elif action.type == "navigation" and "search" in action.target:
                patterns.setdefault("search", {}).setdefault(story.id, 0)
                patterns["search"][story.id] += 1

            # Patrón: Navegación por secciones principales
            elif action.type == "click" and action.target == "a" and action.value in ["User Stories", "Test Cases"]:
                patterns.setdefault("navigation_to_section", {}).setdefault(story.id, 0)
                patterns["navigation_to_section"][story.id] += 1

            # Interacción con contenido destacado
            elif action.type == "click" and action.target == "div" and action.value:
                patterns.setdefault("interaction_with_highlighted_content", {}).setdefault(story.id, 0)
                patterns["interaction_with_highlighted_content"][story.id] += 1

            # Interacciones repetidas
            elif action.type == "click" and action.value == "Test Cases":
                patterns.setdefault("repeated_click", {}).setdefault(story.id, 0)
                patterns["repeated_click"][story.id] += 1

            # Interacción con íconos
            elif action.type == "click" and action.target == "svg":
                patterns.setdefault("ui_icon_interaction", {}).setdefault(story.id, 0)
                patterns["ui_icon_interaction"][story.id] += 1

            # Interacciones ambiguas
            elif action.type == "click" and not action.value:
                patterns.setdefault("ambiguous_interaction", {}).setdefault(story.id, 0)
                patterns["ambiguous_interaction"][story.id] += 1

    return patterns
