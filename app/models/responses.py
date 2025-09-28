"""
Response models for the Forex Chart API.
"""
from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class CandleData(BaseModel):
    """Individual candlestick data point."""
    
    time: datetime = Field(description="Candlestick timestamp")
    open: float = Field(description="Opening price")
    high: float = Field(description="Highest price")
    low: float = Field(description="Lowest price")
    close: float = Field(description="Closing price")


class ChartData(BaseModel):
    """Chart data response."""
    
    pairs: str = Field(description="Currency pair")
    start_date: datetime = Field(description="Data start date")
    end_date: datetime = Field(description="Data end date")
    interval: str = Field(description="Data interval")
    data_points: int = Field(description="Number of data points")
    price_range: Dict[str, float] = Field(description="Price range (min/max)")
    candles: List[CandleData] = Field(description="Candlestick data")


class ChartResponse(BaseModel):
    """Complete chart response."""
    
    success: bool = Field(default=True, description="Request success status")
    message: str = Field(description="Response message")
    chart_data: ChartData = Field(description="Chart data")
    chart_url: Optional[str] = Field(None, description="Interactive chart URL")
    csv_filename: Optional[str] = Field(None, description="CSV export filename")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class ErrorResponse(BaseModel):
    """Error response model."""
    
    success: bool = Field(default=False, description="Request success status")
    error_code: str = Field(description="Error code")
    message: str = Field(description="Error message")
    details: Dict[str, Any] = Field(default_factory=dict, description="Error details")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Error timestamp")


class ChartMetrics(BaseModel):
    """Chart generation metrics."""
    
    data_fetch_time: float = Field(description="Time to fetch data (seconds)")
    chart_generation_time: float = Field(description="Time to generate chart (seconds)")
    total_time: float = Field(description="Total processing time (seconds)")
    data_points_processed: int = Field(description="Number of data points processed")
    memory_usage_mb: Optional[float] = Field(None, description="Peak memory usage in MB")