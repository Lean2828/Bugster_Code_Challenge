from fastapi import APIRouter, Query, HTTPException, Depends
from typing import List, Optional
from models.test import Test
from test_application import generate_tests
from dependencies import get_database_manager
from database_manager import DatabaseManager
from logging_config import logger

router = APIRouter(prefix="/v1/tests")


@router.get("/", summary="Generar tests de Playwright")
async def get_tests_endpoint(
    db_manager: DatabaseManager = Depends(get_database_manager),
    story_id: Optional[str] = Query(None, description="Filtrar por ID de la historia (opcional)"),
) -> List[Test]:
    """
    Endpoint para generar y retornar los tests de Playwright basados en historias.

    Args:
        db_manager (DatabaseManager): Gestor de base de datos.
        story_id (Optional[str]): Identificador único de la historia.

    Returns:
        List[Test]: Lista de tests generados.
    """
    try:
        logger.info(f"Iniciando generación de tests para story_id={story_id}")
        tests = await generate_tests(db_manager=db_manager, story_id=story_id)
        if not tests:
            logger.warning(f"No se encontraron tests para story_id={story_id}")
            raise HTTPException(
                status_code=404,
                detail="No se encontraron tests para los criterios especificados.",
            )
        logger.info(f"Tests generados exitosamente para story_id={story_id}")
        return tests
    except Exception as e:
        logger.error(f"Error generando tests para story_id={story_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error generando tests: {str(e)}",
        )
