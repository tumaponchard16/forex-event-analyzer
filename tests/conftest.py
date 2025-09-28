"""
Test configuration and fixtures.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
import pandas as pd
from datetime import datetime

from app.main import create_app
from app.core.config import get_settings
from app.services.chart_service import ChartService


@pytest.fixture
def app():
    """Create test FastAPI app."""
    return create_app()


@pytest.fixture
def client(app):
    """Create test client."""
    return TestClient(app)


@pytest.fixture
def settings():
    """Get test settings."""
    return get_settings()


@pytest.fixture
def chart_service():
    """Create chart service instance."""
    return ChartService()


@pytest.fixture
def sample_chart_request():
    """Sample chart request data."""
    return {
        "pairs": "EUR/USD",
        "start_date_time": "2025-08-25 10:00 AM",
        "end_date_time": "2025-08-26 10:00 AM",
        "interval": "5m"
    }


@pytest.fixture
def sample_market_data():
    """Sample market data DataFrame."""
    dates = pd.date_range(start='2025-08-25 10:00', end='2025-08-26 10:00', freq='5T')
    data = {
        'Open': [1.1700 + i * 0.0001 for i in range(len(dates))],
        'High': [1.1710 + i * 0.0001 for i in range(len(dates))],
        'Low': [1.1690 + i * 0.0001 for i in range(len(dates))],
        'Close': [1.1705 + i * 0.0001 for i in range(len(dates))]
    }
    df = pd.DataFrame(data, index=dates)
    return df


@pytest.fixture
def mock_yfinance_download(sample_market_data):
    """Mock yfinance download function."""
    with patch('yfinance.download') as mock_download:
        mock_download.return_value = sample_market_data
        yield mock_download


@pytest.fixture
def mock_chart_generation():
    """Mock chart generation."""
    with patch('lightweight_charts.Chart') as mock_chart:
        mock_instance = Mock()
        mock_chart.return_value = mock_instance
        yield mock_instance