import logging
import os
from pathlib import Path

def setup_logger(log_file: str = "logs/app.log") -> logging.Logger:
    """Configura el sistema de logs para registrar eventos y errores en archivo y consola."""
    Path("logs").mkdir(exist_ok=True)

    logger = logging.getLogger("ContentEnricher")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        # Formato detallado de log
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # File Handler
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger