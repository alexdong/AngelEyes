"""Logging configuration for AngelEyes."""

import sys
from pathlib import Path

from loguru import logger

LOG_DIR = Path("/tmp/angeleyes_logs")
LOG_DIR.mkdir(exist_ok=True)

logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO",
)
logger.add(
    LOG_DIR / "angeleyes_{time:YYYY-MM-DD}.log",
    rotation="1 day",
    retention="7 days",
    level="DEBUG",
)

__all__ = ["logger"]
