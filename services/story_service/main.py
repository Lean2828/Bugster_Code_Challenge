from fastapi import FastAPI, Request
from routes.v1.stories import router as stories_router
from database_manager import DatabaseManager
from logging_config import logger
import os
from contextlib import asynccontextmanager

db_uri = os.getenv("DB_URI")
db_name = os.getenv("DB_NAME")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Maneja la conexión y cierre de la base de datos durante el ciclo de vida de la aplicación.

    Args:
        app (FastAPI): Instancia de la aplicación FastAPI.
    """
    global db_manager
    try:
        logger.info("Inicializando conexión a MongoDB...")
        db_manager = DatabaseManager(uri=db_uri, db_name=db_name)
        db_manager.create_indexes()
        logger.info("Conexión a MongoDB inicializada y los índices fueron creados.")
        yield
    except Exception as e:
        logger.error(f"Error en la conexión a MongoDB: {e}", exc_info=True)
    finally:
        if db_manager and db_manager.client:
            db_manager.client.close()
            logger.info("Conexión a MongoDB cerrada.")

app = FastAPI(
    title="Story Service API",
    version="1.0.0",
    description="API para procesar y gestionar historias de usuario",
    lifespan=lifespan,
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Middleware para registrar y manejar errores en las solicitudes.

    Args:
        request (Request): Solicitud HTTP entrante.
        call_next (Callable): Llama al siguiente middleware o endpoint.

    Returns:
        Response: Respuesta generada por la solicitud.
    """
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        logger.error(f"Error procesando la solicitud: {e}", exc_info=True)
        raise e

app.include_router(stories_router)
