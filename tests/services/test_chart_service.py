"""
Tests for the chart service.
"""
import pytest
from unittest.mock import patch, Mock
from datetime import datetime

from app.services.chart_service import ChartService
from app.models.requests import ChartRequest
from app.core.exceptions import (
    DataNotFoundError,
    InvalidDateRangeError,
    ChartGenerationError
)


class TestChartService:
    """Test cases for ChartService."""
    
    def test_parse_date_range_valid(self, chart_service):
        """Test parsing valid date ranges."""
        start_dt, end_dt = chart_service._parse_date_range(
            "2025-08-25 10:00 AM",
            "2025-08-26 10:00 AM"
        )
        
        assert isinstance(start_dt, datetime)
        assert isinstance(end_dt, datetime)
        assert start_dt < end_dt
    
    def test_parse_date_range_invalid_format(self, chart_service):
        """Test parsing invalid date format."""
        with pytest.raises(InvalidDateRangeError):
            chart_service._parse_date_range(
                "invalid-date",
                "2025-08-26 10:00 AM"
            )
    
    def test_parse_date_range_start_after_end(self, chart_service):
        """Test start date after end date."""
        with pytest.raises(InvalidDateRangeError):
            chart_service._parse_date_range(
                "2025-08-26 10:00 AM",
                "2025-08-25 10:00 AM"
            )
    
    def test_parse_date_range_too_large(self, chart_service):
        """Test date range too large."""
        with pytest.raises(InvalidDateRangeError):
            chart_service._parse_date_range(
                "2025-01-01 10:00 AM",
                "2025-12-31 10:00 AM"
            )
    
    def test_fetch_market_data_success(self, chart_service, mock_yfinance_download, sample_market_data):
        """Test successful market data fetch."""
        start_dt = datetime(2025, 8, 25, 10, 0)
        end_dt = datetime(2025, 8, 26, 10, 0)
        
        df = chart_service._fetch_market_data("EUR/USD", start_dt, end_dt, "5m")
        
        assert not df.empty
        assert len(df) == len(sample_market_data)
        mock_yfinance_download.assert_called()
    
    def test_fetch_market_data_no_data(self, chart_service):
        """Test market data fetch with no data."""
        with patch('yfinance.download') as mock_download:
            mock_download.return_value = None
            
            with pytest.raises(DataNotFoundError):
                start_dt = datetime(2025, 8, 25, 10, 0)
                end_dt = datetime(2025, 8, 26, 10, 0)
                chart_service._fetch_market_data("INVALID/PAIR", start_dt, end_dt, "5m")
    
    def test_process_chart_data(self, chart_service, sample_market_data):
        """Test chart data processing."""
        start_dt = datetime(2025, 8, 25, 10, 0)
        end_dt = datetime(2025, 8, 26, 10, 0)
        
        chart_data = chart_service._process_chart_data(
            sample_market_data, "EUR/USD", start_dt, end_dt, "5m"
        )
        
        assert chart_data.pairs == "EUR/USD"
        assert chart_data.interval == "5m"
        assert chart_data.data_points > 0
        assert len(chart_data.candles) > 0
        assert "min" in chart_data.price_range
        assert "max" in chart_data.price_range
    
    def test_generate_chart_success(self, chart_service, mock_yfinance_download, mock_chart_generation):
        """Test successful chart generation."""
        request = ChartRequest(
            pairs="EUR/USD",
            start_date_time="2025-08-25 10:00 AM",
            end_date_time="2025-08-26 10:00 AM",
            interval="5m"
        )
        
        response = chart_service.generate_chart(request, generate_interactive=False)
        
        assert response.success is True
        assert response.chart_data is not None
        assert response.chart_data.pairs == "EUR/USD"
        assert "metrics" in response.metadata
    
    def test_generate_chart_with_interactive(self, chart_service, mock_yfinance_download, mock_chart_generation):
        """Test chart generation with interactive chart."""
        request = ChartRequest(
            pairs="EUR/USD",
            start_date_time="2025-08-25 10:00 AM",
            end_date_time="2025-08-26 10:00 AM",
            interval="5m"
        )
        
        with patch.object(chart_service, '_generate_interactive_chart') as mock_interactive:
            mock_interactive.return_value = ("http://localhost:5500", "test.csv")
            
            response = chart_service.generate_chart(request, generate_interactive=True)
            
            assert response.success is True
            assert response.chart_url is not None
            assert response.csv_filename is not None
    
    def test_generate_chart_data_not_found(self, chart_service):
        """Test chart generation with no data found."""
        request = ChartRequest(
            pairs="INVALID/PAIR",
            start_date_time="2025-08-25 10:00 AM",
            end_date_time="2025-08-26 10:00 AM",
            interval="5m"
        )
        
        with patch('yfinance.download') as mock_download:
            mock_download.return_value = None
            
            with pytest.raises(ChartGenerationError):
                chart_service.generate_chart(request)