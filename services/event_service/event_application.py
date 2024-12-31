import httpx
import asyncio
import os
from dotenv import load_dotenv
from typing import List
from models.event import Event
from database_manager import DatabaseManager
from logging_config import logger

load_dotenv()
STORIES_SERVICE_URL = os.getenv("STORIES_SERVICE_URL")

async def notify_stories_service(events: List[Event]):
    """
    Envía una notificación al servicio de historias con los eventos procesados.
    """
    if not STORIES_SERVICE_URL:
        logger.warning("STORIES_SERVICE_URL no configurado. No se enviaron notificaciones.")
        return

    events_json = [event.to_json() for event in events]
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(url=STORIES_SERVICE_URL, json=events_json)
            if response.status_code != 200:
                logger.error(f"Error llamando al servicio de historias: {response.text}")
    except httpx.RequestError as e:
        logger.error(f"Error conectando con el servicio de historias: {str(e)}")

async def process_events(events: List[Event], db_manager: DatabaseManager) -> dict:
    """
    Procesa eventos, los guarda en MongoDB y actualiza la tabla `sessions`.
    
    Args:
        events (List[Event]): Lista de eventos (instancias de la clase Event).
        db_manager (DatabaseManager): Instancia para interactuar con la base de datos.
    
    Returns:
        dict: Resumen del estado del procesamiento.
    """
    if not events:
        raise ValueError("No se proporcionaron eventos.")

    sessions_data = {}
    for event in events:
        distinct_id = event.properties.distinct_id
        session_id = event.properties.session_id
        if distinct_id not in sessions_data:
            sessions_data[distinct_id] = set()
        sessions_data[distinct_id].add(session_id)

    formatted_sessions = [
        {"distinct_id": distinct_id, "sessions": list(session_ids)}
        for distinct_id, session_ids in sessions_data.items()
    ]

    try:
        db_manager.bulk_save_events(events)
        db_manager.bulk_upsert_sessions(formatted_sessions)
        
        await notify_stories_service(events)
    except Exception as e:
        logger.error(f"Error al procesar eventos: {str(e)}", exc_info=True)
        raise

    return {
        "status": "success",
        "message": f"{len(events)} eventos procesados correctamente.",
    }


