from fastapi import APIRouter, HTTPException, Body, Depends
from typing import List
from models.event import Event
from event_application import process_events
from dependencies import get_database_manager
from database_manager import DatabaseManager
from logging_config import logger

router = APIRouter(prefix="/v1/events")

@router.post("/", summary="Procesar eventos")
async def process_events_route(
    events: List[Event] = Body(..., description="Lista de eventos"),
    db_manager: DatabaseManager = Depends(get_database_manager),
):
    """
    Procesa eventos, guarda en MongoDB y actualiza sesiones.
    """
    if not events:
        raise HTTPException(status_code=400, detail="No se proporcionaron eventos.")

    try:
        result = await process_events(events, db_manager)
        return result
    except Exception as e:
        logger.error(f"Error procesando eventos: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error interno procesando eventos.")
