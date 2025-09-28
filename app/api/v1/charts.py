"""
Version 1 API endpoints for forex charts.
"""
from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse

from app.core.config import get_settings, Settings
from app.core.exceptions import (
    ForexChartException,
    DataNotFoundError,
    InvalidDateRangeError,
    InvalidCurrencyPairError,
    ChartGenerationError
)
from app.core.logging import get_logger
from app.models.requests import ChartRequest, HealthCheck
from app.models.responses import ChartResponse, ErrorResponse
from app.services.chart_service import ChartService

router = APIRouter(prefix="/v1", tags=["Charts v1"])
logger = get_logger(__name__)


def get_chart_service() -> ChartService:
    """Dependency to get chart service instance."""
    return ChartService()


@router.post(
    "/charts",
    response_model=ChartResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        404: {"model": ErrorResponse, "description": "Data Not Found"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    },
    summary="Generate Forex Chart",
    description="Generate an interactive forex chart with historical data"
)
async def create_chart(
    request: ChartRequest,
    chart_service: ChartService = Depends(get_chart_service)
) -> ChartResponse:
    """
    Generate a forex chart for the specified currency pair and date range.
    
    - **pairs**: Currency pair (e.g., "EUR/USD")
    - **start_date_time**: Start date and time 
    - **end_date_time**: End date and time
    - **interval**: Data interval (1m, 5m, 15m, 30m, 1h, 1d)
    """
    try:
        logger.info(f"Creating chart for {request.pairs}")
        result = chart_service.generate_chart(request, generate_interactive=True)
        return result
        
    except (DataNotFoundError, InvalidDateRangeError, InvalidCurrencyPairError) as e:
        logger.warning(f"Client error: {e}")
        raise HTTPException(
            status_code=400 if isinstance(e, (InvalidDateRangeError, InvalidCurrencyPairError)) else 404,
            detail={
                "error_code": e.error_code,
                "message": e.message,
                "details": e.details
            }
        )
    except ChartGenerationError as e:
        logger.error(f"Chart generation error: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "error_code": e.error_code,
                "message": e.message,
                "details": e.details
            }
        )
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "error_code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred",
                "details": {"error": str(e)}
            }
        )


@router.post(
    "/charts/data-only",
    response_model=ChartResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        404: {"model": ErrorResponse, "description": "Data Not Found"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    },
    summary="Get Chart Data Only",
    description="Get chart data without generating interactive chart"
)
async def get_chart_data(
    request: ChartRequest,
    chart_service: ChartService = Depends(get_chart_service)
) -> ChartResponse:
    """
    Get chart data for the specified currency pair and date range without generating interactive chart.
    
    This endpoint is useful when you only need the raw data for analysis.
    """
    try:
        logger.info(f"Getting chart data for {request.pairs}")
        result = chart_service.generate_chart(request, generate_interactive=False)
        return result
        
    except (DataNotFoundError, InvalidDateRangeError, InvalidCurrencyPairError) as e:
        logger.warning(f"Client error: {e}")
        raise HTTPException(
            status_code=400 if isinstance(e, (InvalidDateRangeError, InvalidCurrencyPairError)) else 404,
            detail={
                "error_code": e.error_code,
                "message": e.message,
                "details": e.details
            }
        )
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "error_code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred",
                "details": {"error": str(e)}
            }
        )


@router.get(
    "/health",
    response_model=HealthCheck,
    summary="Health Check",
    description="Check API health status"
)
async def health_check(settings: Settings = Depends(get_settings)) -> HealthCheck:
    """Check the health status of the API."""
    return HealthCheck(
        status="healthy",
        version=settings.api_version
    )


@router.get(
    "/supported-pairs",
    summary="Get Supported Currency Pairs",
    description="Get list of commonly supported currency pairs"
)
async def get_supported_pairs() -> Dict[str, Any]:
    """Get list of commonly supported currency pairs."""
    return {
        "major_pairs": [
            "EUR/USD", "GBP/USD", "USD/JPY", "USD/CHF",
            "AUD/USD", "USD/CAD", "NZD/USD"
        ],
        "cross_pairs": [
            "EUR/GBP", "EUR/JPY", "GBP/JPY", "AUD/JPY",
            "EUR/CHF", "GBP/CHF", "CHF/JPY"
        ],
        "note": "Other pairs may be available. The API automatically tries multiple ticker formats."
    }


@router.get(
    "/intervals",
    summary="Get Supported Intervals",
    description="Get list of supported data intervals"
)
async def get_supported_intervals() -> Dict[str, Any]:
    """Get list of supported data intervals."""
    return {
        "intervals": [
            {"code": "1m", "description": "1 minute"},
            {"code": "5m", "description": "5 minutes"},
            {"code": "15m", "description": "15 minutes"},
            {"code": "30m", "description": "30 minutes"},
            {"code": "1h", "description": "1 hour"},
            {"code": "1d", "description": "1 day"}
        ],
        "default": "5m",
        "note": "Shorter intervals may have limited historical data availability."
    }