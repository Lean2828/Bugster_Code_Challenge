from logging_config import logger
from fastapi import APIRouter, HTTPException, Depends
from typing import Optional, List
from models.event import Event
from database_manager import DatabaseManager
from dependencies import get_database_manager
from story_application import (
    get_stories,
    post_stories,
    get_patterns,
)

router = APIRouter(prefix="/v1/stories")

@router.get("/", summary="Obtener historias de usuario")
async def get_stories_endpoint(
    session_id: Optional[str] = None,
    story_id: Optional[str] = None,
    db_manager: DatabaseManager = Depends(get_database_manager),
):
    """
    Obtiene historias de usuario desde la base de datos.
    """
    try:
        logger.info(f"Recibiendo solicitud GET /v1/stories con session_id={session_id} y story_id={story_id}")

        # Llamada a la capa de aplicación
        stories = await get_stories(db_manager, session_id, story_id)

        # Validación si no se encontraron historias
        if not stories:
            logger.warning(f"No se encontraron historias para session_id={session_id}, story_id={story_id}")
            raise HTTPException(status_code=404, detail="No stories found.")

        logger.info(f"Historias obtenidas exitosamente: {len(stories)} historias encontradas.")
        return {"stories": stories}

    except HTTPException as http_exc:
        logger.error(f"Error HTTP al procesar solicitud GET /v1/stories: {http_exc.detail}")
        raise http_exc

    except Exception as e:
        logger.error(f"Error inesperado al procesar solicitud GET /v1/stories: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error retrieving stories: {str(e)}")



@router.post("/", summary="Crear o actualizar historias")
async def post_stories_endpoint(
    events: List[Event],
    db_manager: DatabaseManager = Depends(get_database_manager),
):
    """
    Crea o actualiza historias basadas en una lista de eventos.

    Args:
        events (List[Event]): Lista de eventos proporcionados.
        db_manager (DatabaseManager): Gestor de la base de datos.

    Returns:
        dict: Mensaje de confirmación del éxito de la operación.
    """
    try:
        if not events:
            raise HTTPException(status_code=400, detail="No events provided.")
        await post_stories(events, db_manager)
        return {"message": "Stories created or updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing stories: {str(e)}")

@router.get("/patterns", summary="Identificar patrones comunes en historias")
async def get_patterns_endpoint(
    session_id: Optional[str] = None,
    db_manager: DatabaseManager = Depends(get_database_manager),
):
    """
    Identifica patrones comunes en las historias almacenadas.

    Args:
        session_id (Optional[str]): ID de sesión para filtrar historias.

    Returns:
        dict: Diccionario de patrones detectados.
    """
    try:
        return await get_patterns(db_manager, session_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving patterns: {str(e)}")
