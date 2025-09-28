"""
Logging configuration for the Forex Chart API.
"""
import logging
import sys
from typing import Dict, Any

from app.core.config import get_settings


def setup_logging() -> None:
    """Set up logging configuration."""
    settings = get_settings()
    
    logging.basicConfig(
        level=getattr(logging, settings.log_level),
        format=settings.log_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
        ]
    )
    
    # Set third-party loggers to WARNING to reduce noise
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("yfinance").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance."""
    return logging.getLogger(name)


class LoggerMixin:
    """Mixin class to add logging capabilities."""
    
    @property
    def logger(self) -> logging.Logger:
        return get_logger(self.__class__.__name__)