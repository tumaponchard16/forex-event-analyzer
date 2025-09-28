"""
Tests for the API endpoints.
"""
import pytest
from unittest.mock import patch, Mock

from app.models.responses import ChartResponse, ChartData, CandleData


class TestChartsAPI:
    """Test cases for Charts API endpoints."""
    
    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/api/v1/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "timestamp" in data
    
    def test_supported_pairs(self, client):
        """Test supported pairs endpoint."""
        response = client.get("/api/v1/supported-pairs")
        
        assert response.status_code == 200
        data = response.json()
        assert "major_pairs" in data
        assert "cross_pairs" in data
        assert isinstance(data["major_pairs"], list)
        assert "EUR/USD" in data["major_pairs"]
    
    def test_supported_intervals(self, client):
        """Test supported intervals endpoint."""
        response = client.get("/api/v1/intervals")
        
        assert response.status_code == 200
        data = response.json()
        assert "intervals" in data
        assert "default" in data
        assert isinstance(data["intervals"], list)
        assert data["default"] == "5m"
    
    def test_create_chart_success(self, client, sample_chart_request, mock_yfinance_download):
        """Test successful chart creation."""
        with patch('app.services.chart_service.ChartService.generate_chart') as mock_generate:
            # Mock successful response
            mock_response = ChartResponse(
                message="Chart created successfully",
                chart_data=ChartData(
                    pairs="EUR/USD",
                    start_date="2025-08-25T10:00:00",
                    end_date="2025-08-26T10:00:00",
                    interval="5m",
                    data_points=100,
                    price_range={"min": 1.1700, "max": 1.1800},
                    candles=[]
                ),
                chart_url="http://localhost:5500",
                csv_filename="test.csv",
                metadata={"metrics": {"total_time": 1.5}}
            )
            mock_generate.return_value = mock_response
            
            response = client.post("/api/v1/charts", json=sample_chart_request)
            
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert data["chart_data"]["pairs"] == "EUR/USD"
            assert "chart_url" in data
    
    def test_create_chart_invalid_pairs(self, client):
        """Test chart creation with invalid pairs."""
        request_data = {
            "pairs": "INVALID",  # Missing /
            "start_date_time": "2025-08-25 10:00 AM",
            "end_date_time": "2025-08-26 10:00 AM",
            "interval": "5m"
        }
        
        response = client.post("/api/v1/charts", json=request_data)
        
        assert response.status_code == 422  # Validation error
    
    def test_create_chart_invalid_interval(self, client):
        """Test chart creation with invalid interval."""
        request_data = {
            "pairs": "EUR/USD",
            "start_date_time": "2025-08-25 10:00 AM",
            "end_date_time": "2025-08-26 10:00 AM",
            "interval": "invalid"
        }
        
        response = client.post("/api/v1/charts", json=request_data)
        
        assert response.status_code == 422  # Validation error
    
    def test_create_chart_invalid_date_format(self, client):
        """Test chart creation with invalid date format."""
        request_data = {
            "pairs": "EUR/USD",
            "start_date_time": "invalid-date",
            "end_date_time": "2025-08-26 10:00 AM",
            "interval": "5m"
        }
        
        response = client.post("/api/v1/charts", json=request_data)
        
        assert response.status_code == 422  # Validation error
    
    def test_get_chart_data_only(self, client, sample_chart_request, mock_yfinance_download):
        """Test getting chart data without interactive chart."""
        with patch('app.services.chart_service.ChartService.generate_chart') as mock_generate:
            # Mock successful response without chart URL
            mock_response = ChartResponse(
                message="Chart data retrieved successfully",
                chart_data=ChartData(
                    pairs="EUR/USD",
                    start_date="2025-08-25T10:00:00",
                    end_date="2025-08-26T10:00:00",
                    interval="5m",
                    data_points=100,
                    price_range={"min": 1.1700, "max": 1.1800},
                    candles=[]
                ),
                chart_url=None,
                csv_filename=None,
                metadata={"metrics": {"total_time": 0.8}}
            )
            mock_generate.return_value = mock_response
            
            response = client.post("/api/v1/charts/data-only", json=sample_chart_request)
            
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert data["chart_data"]["pairs"] == "EUR/USD"
            assert data["chart_url"] is None
    
    def test_root_endpoint(self, client):
        """Test root endpoint."""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "docs_url" in data
        assert data["docs_url"] == "/docs"
    
    def test_create_chart_data_not_found(self, client, sample_chart_request):
        """Test chart creation when data not found."""
        from app.core.exceptions import DataNotFoundError
        
        with patch('app.services.chart_service.ChartService.generate_chart') as mock_generate:
            mock_generate.side_effect = DataNotFoundError(
                "No data found for EUR/USD",
                details={"pairs": "EUR/USD"}
            )
            
            response = client.post("/api/v1/charts", json=sample_chart_request)
            
            assert response.status_code == 404
            data = response.json()
            assert "error_code" in data["detail"]
            assert data["detail"]["error_code"] == "DATA_NOT_FOUND"
    
    def test_create_chart_internal_error(self, client, sample_chart_request):
        """Test chart creation with internal error."""
        with patch('app.services.chart_service.ChartService.generate_chart') as mock_generate:
            mock_generate.side_effect = Exception("Internal server error")
            
            response = client.post("/api/v1/charts", json=sample_chart_request)
            
            assert response.status_code == 500
            data = response.json()
            assert "error_code" in data["detail"]
            assert data["detail"]["error_code"] == "INTERNAL_ERROR"