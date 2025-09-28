"""
Request models for the Forex Chart API.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator, Field


class ChartRequest(BaseModel):
    """Request model for chart generation."""
    
    pairs: str = Field(
        ...,
        description="Currency pair in format 'BASE/QUOTE' (e.g., 'EUR/USD')",
        example="EUR/USD"
    )
    start_date_time: str = Field(
        ...,
        description="Start datetime in format 'YYYY-MM-DD HH:MM AM/PM' or 'YYYY-MM-DD HH:MM'",
        example="2025-08-25 10:00 AM"
    )
    end_date_time: str = Field(
        ...,
        description="End datetime in format 'YYYY-MM-DD HH:MM AM/PM' or 'YYYY-MM-DD HH:MM'",
        example="2025-08-26 10:00 AM"
    )
    interval: str = Field(
        default="5m",
        description="Data interval",
        example="5m"
    )
    
    @field_validator('pairs')
    @classmethod
    def validate_pairs(cls, v):
        if '/' not in v:
            raise ValueError('Currency pair must contain "/" (e.g., EUR/USD)')
        parts = v.split('/')
        if len(parts) != 2:
            raise ValueError('Currency pair must have exactly one "/" separator')
        base, quote = parts
        if len(base) != 3 or len(quote) != 3:
            raise ValueError('Each currency code must be exactly 3 characters')
        return v.upper()
    
    @field_validator('interval')
    @classmethod
    def validate_interval(cls, v):
        allowed_intervals = ['1m', '5m', '15m', '30m', '1h', '1d']
        if v not in allowed_intervals:
            raise ValueError(f'interval must be one of {allowed_intervals}')
        return v
    
    @field_validator('start_date_time', 'end_date_time')
    @classmethod
    def validate_datetime_format(cls, v):
        formats = [
            "%Y-%m-%d %I:%M %p",    # 2025-08-25 10:00 AM
            "%Y-%m-%d %H:%M",       # 2025-08-25 10:00 (24-hour)
            "%Y-%m-%d %I:%M%p",     # 2025-08-25 10:00AM (no space)
        ]
        
        for fmt in formats:
            try:
                datetime.strptime(v, fmt)
                return v
            except ValueError:
                continue
        
        raise ValueError(
            "Datetime format must be 'YYYY-MM-DD HH:MM AM/PM' or 'YYYY-MM-DD HH:MM'"
        )


class HealthCheck(BaseModel):
    """Health check response model."""
    
    status: str = Field(default="healthy", description="Service status")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Check timestamp")
    version: str = Field(description="API version")
    uptime: Optional[float] = Field(None, description="Service uptime in seconds")