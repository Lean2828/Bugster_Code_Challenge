import logging
from logging.handlers import RotatingFileHandler
import os

# Crear directorio para los logs si no existe
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Configuración del logger
LOG_FILE = os.path.join(LOG_DIR, "app.log")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_LEVEL = logging.INFO

# Configurar el logger
logger = logging.getLogger("bugster_logger")
logger.setLevel(LOG_LEVEL)

# Configurar el handler para archivo
file_handler = RotatingFileHandler(LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=3)
file_handler.setLevel(LOG_LEVEL)
file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

# Configurar el handler para consola
console_handler = logging.StreamHandler()
console_handler.setLevel(LOG_LEVEL)
console_handler.setFormatter(logging.Formatter(LOG_FORMAT))

# Agregar handlers al logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)
