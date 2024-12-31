from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from routes.v1.events import router as events_router
from database_manager import DatabaseManager
import os
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("event_service")

db_uri = os.getenv("DB_URI")
db_name = os.getenv("DB_NAME")

@asynccontextmanager
async def lifespan(app: FastAPI):
    global db_manager
    try:
        logger.info("Inicializando conexión a MongoDB...")
        db_manager = DatabaseManager(uri=db_uri, db_name=db_name)
        db_manager.create_indexes()
        logger.info("Conexión a MongoDB inicializada y los índices fueron creados.")
        yield
    except Exception as e:
        logger.error(f"Error en la conexión a MongoDB: {e}")
    finally:
        if db_manager and db_manager.client:
            db_manager.client.close()
            logger.info("Conexión a MongoDB cerrada.")

app = FastAPI(
    title="Event Processing API",
    version="1.0.0",
    description="API para procesar y almacenar eventos en MongoDB",
    lifespan=lifespan
)

app.include_router(events_router)
