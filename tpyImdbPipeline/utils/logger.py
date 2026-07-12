import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler


load_dotenv()


def get_logger(
    name: str,
    log_directory: Path = Path(os.getenv("LOG_PATH")),
    log_file: str = os.getenv("LOG_FILE_NAME"),
    level: int = logging.INFO,
) -> logging.Logger:
    """
    Creates and returns a configured logger.
    Features:
    - Console logging
    - Rotating file logging
    - 10 MB max log size
    - Retains last 10 log files
    - Timestamp, log level, logger name, message
    """

    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(level)
    logger.propagate = False
    log_directory.mkdir(parents=True, exist_ok=True)
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    # Rotating File Handler
    file_handler = RotatingFileHandler(
        filename=log_directory / log_file,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=10,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger