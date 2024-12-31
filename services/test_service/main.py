import os
from fastapi import FastAPI
from routes.v1.tests import router as tests_router
from contextlib import asynccontextmanager
from database_manager import DatabaseManager
from logging_config import logger

db_uri = os.getenv("DB_URI")
db_name = os.getenv("DB_NAME")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Configura el ciclo de vida de la aplicación FastAPI, incluyendo la inicialización y cierre de la base de datos.
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
        raise e
    finally:
        if db_manager and db_manager.client:
            db_manager.client.close()
            logger.info("Conexión a MongoDB cerrada.")


app = FastAPI(
    title="Test Service API",
    version="1.0.0",
    description="API para generar tests de Playwright basados en historias de usuario",
    lifespan=lifespan,
)

@app.middleware("http")
async def log_requests(request, call_next):
    """
    Middleware para loggear cada solicitud HTTP.
    """
    logger.info(f"Recibiendo solicitud: {request.method} {request.url}")
    try:
        response = await call_next(request)
        logger.info(f"Solicitud completada con código {response.status_code}")
        return response
    except Exception as e:
        logger.error(f"Error procesando solicitud: {e}", exc_info=True)
        raise e


app.include_router(tests_router)
