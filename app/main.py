"""
Main FastAPI application.
"""
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api import api_router
from app.core.config import get_settings
from app.core.logging import setup_logging, get_logger
from app.core.exceptions import ForexChartException

# Setup logging
setup_logging()
logger = get_logger(__name__)

# Application startup time for uptime calculation
app_start_time = time.time()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info("🚀 Forex Chart API is starting up...")
    settings = get_settings()
    logger.info(f"📊 API Version: {settings.api_version}")
    logger.info(f"🔧 Debug Mode: {settings.debug}")
    
    yield
    
    # Shutdown
    logger.info("👋 Forex Chart API is shutting down...")


def create_app() -> FastAPI:
    """Create FastAPI application."""
    settings = get_settings()
    
    app = FastAPI(
        title=settings.api_title,
        description=settings.api_description,
        version=settings.api_version,
        debug=settings.debug,
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=settings.cors_allow_methods,
        allow_headers=settings.cors_allow_headers,
    )
    
    # Add request logging middleware
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start_time = time.time()
        
        # Log request
        logger.info(f"📨 {request.method} {request.url.path}")
        
        # Process request
        response = await call_next(request)
        
        # Log response
        process_time = time.time() - start_time
        logger.info(
            f"📤 {request.method} {request.url.path} - "
            f"Status: {response.status_code} - "
            f"Time: {process_time:.3f}s"
        )
        
        return response
    
    # Global exception handler for ForexChartException
    @app.exception_handler(ForexChartException)
    async def forex_chart_exception_handler(request: Request, exc: ForexChartException):
        logger.error(f"ForexChartException: {exc.message}")
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "error_code": exc.error_code,
                "message": exc.message,
                "details": exc.details
            }
        )
    
    # Include API routes
    app.include_router(api_router)
    
    # Root endpoint
    @app.get("/", tags=["Root"])
    async def root():
        """Root endpoint with API information."""
        return {
            "message": "Forex Chart API",
            "version": settings.api_version,
            "docs_url": "/docs",
            "health_check": "/api/v1/health",
            "uptime_seconds": time.time() - app_start_time
        }
    
    return app


# Create the application instance
app = create_app()