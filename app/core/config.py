"""
Configuration management for the Forex Chart API.
"""
from functools import lru_cache
from typing import Optional
from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # API Configuration
    api_title: str = "Forex Chart API"
    api_description: str = "Interactive forex charts with historical data"
    api_version: str = "1.0.0"
    debug: bool = False
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = False
    
    # Chart Configuration
    default_interval: str = "5m"
    max_days_lookback: int = 30
    chart_width: int = 1400
    chart_height: int = 700
    chart_server_port: int = 5500
    
    # Data Source Configuration
    yfinance_timeout: int = 30
    max_data_points: int = 10000
    
    # CORS Configuration
    cors_origins: list = ["*"]
    cors_allow_credentials: bool = True
    cors_allow_methods: list = ["*"]
    cors_allow_headers: list = ["*"]
    
    # Logging Configuration
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    @field_validator('log_level')
    @classmethod
    def validate_log_level(cls, v):
        allowed_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if v.upper() not in allowed_levels:
            raise ValueError(f'log_level must be one of {allowed_levels}')
        return v.upper()
    
    @field_validator('default_interval')
    @classmethod
    def validate_interval(cls, v):
        allowed_intervals = ['1m', '5m', '15m', '30m', '1h', '1d']
        if v not in allowed_intervals:
            raise ValueError(f'default_interval must be one of {allowed_intervals}')
        return v
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": False
    }


@lru_cache()
def get_settings() -> Settings:
    """Get cached application settings."""
    return Settings()