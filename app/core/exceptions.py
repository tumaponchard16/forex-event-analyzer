"""
Custom exceptions for the Forex Chart API.
"""
from typing import Any, Dict, Optional


class ForexChartException(Exception):
    """Base exception for forex chart operations."""
    
    def __init__(
        self,
        message: str,
        error_code: str = "GENERAL_ERROR",
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)


class DataNotFoundError(ForexChartException):
    """Raised when no data is found for the requested parameters."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="DATA_NOT_FOUND",
            details=details
        )


class InvalidDateRangeError(ForexChartException):
    """Raised when the date range is invalid."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="INVALID_DATE_RANGE",
            details=details
        )


class InvalidCurrencyPairError(ForexChartException):
    """Raised when the currency pair is invalid."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="INVALID_CURRENCY_PAIR",
            details=details
        )


class ChartGenerationError(ForexChartException):
    """Raised when chart generation fails."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="CHART_GENERATION_ERROR",
            details=details
        )