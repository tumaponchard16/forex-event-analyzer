"""
Chart service for generating interactive forex charts.
"""
import time
import os
import platform
import webbrowser
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple, Optional
import pandas as pd
import yfinance as yf
from lightweight_charts import Chart

from ..core.config import get_settings
from ..core.exceptions import (
    DataNotFoundError,
    InvalidDateRangeError,
    InvalidCurrencyPairError,
    ChartGenerationError
)
from ..core.logging import LoggerMixin
from ..models.requests import ChartRequest
from ..models.responses import ChartData, ChartResponse, CandleData, ChartMetrics


class ChartService(LoggerMixin):
    """Service for generating forex charts."""
    
    def __init__(self):
        self.settings = get_settings()
    
    def generate_chart(
        self, 
        request: ChartRequest, 
        generate_interactive: bool = True
    ) -> ChartResponse:
        """
        Generate a forex chart based on the request parameters.
        
        Args:
            request: Chart generation request
            generate_interactive: Whether to generate an interactive chart
            
        Returns:
            ChartResponse with chart data and metadata
        """
        start_time = time.time()
        
        try:
            self.logger.info(f"Generating chart for {request.pairs} from {request.start_date_time} to {request.end_date_time}")
            
            # Parse and validate date range
            start_dt, end_dt = self._parse_date_range(
                request.start_date_time, 
                request.end_date_time
            )
            
            # Fetch market data
            fetch_start_time = time.time()
            df = self._fetch_market_data(
                request.pairs, 
                start_dt, 
                end_dt, 
                request.interval
            )
            fetch_time = time.time() - fetch_start_time
            
            # Process data for chart
            chart_data = self._process_chart_data(df, request.pairs, start_dt, end_dt, request.interval)
            
            # Generate interactive chart if requested
            chart_url = None
            csv_filename = None
            
            if generate_interactive:
                chart_gen_start_time = time.time()
                chart_url, csv_filename = self._generate_interactive_chart(
                    df, 
                    request.pairs, 
                    start_dt, 
                    end_dt
                )
                chart_gen_time = time.time() - chart_gen_start_time
            else:
                chart_gen_time = 0
            
            total_time = time.time() - start_time
            
            # Create metrics
            metrics = ChartMetrics(
                data_fetch_time=fetch_time,
                chart_generation_time=chart_gen_time,
                total_time=total_time,
                data_points_processed=len(df)
            )
            
            self.logger.info(f"Chart generated successfully in {total_time:.2f}s with {len(df)} data points")
            
            return ChartResponse(
                message=f"Chart created successfully for {request.pairs}",
                chart_data=chart_data,
                chart_url=chart_url,
                csv_filename=csv_filename,
                metadata={
                    "metrics": metrics.dict(),
                    "settings": {
                        "interval": request.interval,
                        "data_points": len(df),
                        "date_range": f"{start_dt} to {end_dt}"
                    }
                }
            )
            
        except Exception as e:
            self.logger.error(f"Chart generation failed: {str(e)}")
            raise ChartGenerationError(
                message=f"Failed to generate chart: {str(e)}",
                details={
                    "pairs": request.pairs,
                    "start_date": request.start_date_time,
                    "end_date": request.end_date_time,
                    "interval": request.interval
                }
            )
    
    def _parse_date_range(self, start_str: str, end_str: str) -> Tuple[datetime, datetime]:
        """Parse and validate date range."""
        formats = [
            "%Y-%m-%d %I:%M %p",    # 2025-08-25 10:00 AM
            "%Y-%m-%d %H:%M",       # 2025-08-25 10:00 (24-hour)
            "%Y-%m-%d %I:%M%p",     # 2025-08-25 10:00AM (no space)
        ]
        
        def parse_datetime(date_str: str) -> datetime:
            for fmt in formats:
                try:
                    return datetime.strptime(date_str, fmt)
                except ValueError:
                    continue
            raise InvalidDateRangeError(f"Unable to parse datetime: {date_str}")
        
        start_dt = parse_datetime(start_str)
        end_dt = parse_datetime(end_str)
        
        if start_dt >= end_dt:
            raise InvalidDateRangeError("Start date must be before end date")
        
        # Check if date range is too large
        if (end_dt - start_dt).days > self.settings.max_days_lookback:
            raise InvalidDateRangeError(
                f"Date range too large. Maximum allowed: {self.settings.max_days_lookback} days"
            )
        
        return start_dt, end_dt
    
    def _fetch_market_data(
        self, 
        pairs: str, 
        start_dt: datetime, 
        end_dt: datetime, 
        interval: str
    ) -> pd.DataFrame:
        """Fetch market data from Yahoo Finance."""
        pair_clean = pairs.upper().replace(' ', '')
        base, quote = pair_clean.split('/')
        
        candidates = [
            pair_clean.replace('/', '') + '=X',  # EURUSD=X
            base + quote + '=X',                 # EURUSD=X (same)
            quote + base + '=X',                 # USDEUR=X (fallback)
            quote + '=X'                         # sometimes JPY=X works for USD/JPY
        ]
        
        df = None
        used_symbol = None
        
        for sym in candidates:
            try:
                self.logger.debug(f"Trying to fetch data for symbol: {sym}")
                df_try = yf.download(
                    sym, 
                    start=start_dt, 
                    end=end_dt, 
                    interval=interval, 
                    progress=False, 
                    auto_adjust=True,
                    timeout=self.settings.yfinance_timeout
                )
                
                if df_try is not None and isinstance(df_try, pd.DataFrame) and not df_try.empty:
                    df = df_try
                    used_symbol = sym
                    self.logger.info(f"Successfully fetched data using symbol: {sym}")
                    break
                    
            except Exception as e:
                self.logger.warning(f"Failed to download {sym}: {e}")
                continue
        
        if df is None or df.empty:
            raise DataNotFoundError(
                f"No data found for {pairs}",
                details={
                    "pairs": pairs,
                    "candidates_tried": candidates,
                    "start_date": start_dt.isoformat(),
                    "end_date": end_dt.isoformat(),
                    "interval": interval
                }
            )
        
        # Remove duplicate timestamps
        df = df[~df.index.duplicated(keep='first')]
        
        # Check if we have enough data points
        if len(df) > self.settings.max_data_points:
            self.logger.warning(f"Data points ({len(df)}) exceed maximum ({self.settings.max_data_points})")
            df = df.tail(self.settings.max_data_points)
        
        return df
    
    def _process_chart_data(
        self, 
        df: pd.DataFrame, 
        pairs: str, 
        start_dt: datetime, 
        end_dt: datetime, 
        interval: str
    ) -> ChartData:
        """Process DataFrame into ChartData model."""
        candles = []
        
        for idx, row in df.iterrows():
            def safe_float(value):
                if hasattr(value, 'iloc'):
                    return float(value.iloc[0])
                elif pd.isna(value):
                    return None
                else:
                    return float(value)
            
            # Skip rows with any NaN values
            open_val = safe_float(row["Open"])
            high_val = safe_float(row["High"])
            low_val = safe_float(row["Low"])
            close_val = safe_float(row["Close"])
            
            if None not in [open_val, high_val, low_val, close_val]:
                candles.append(CandleData(
                    time=idx,
                    open=open_val,
                    high=high_val,
                    low=low_val,
                    close=close_val
                ))
        
        if not candles:
            raise DataNotFoundError("No valid data points found after processing")
        
        # Calculate price range
        all_prices = []
        for candle in candles:
            all_prices.extend([candle.open, candle.high, candle.low, candle.close])
        
        price_range = {
            "min": min(all_prices),
            "max": max(all_prices)
        }
        
        return ChartData(
            pairs=pairs,
            start_date=df.index.min(),
            end_date=df.index.max(),
            interval=interval,
            data_points=len(candles),
            price_range=price_range,
            candles=candles
        )
    
    def _generate_interactive_chart(
        self, 
        df: pd.DataFrame, 
        pairs: str, 
        start_dt: datetime, 
        end_dt: datetime
    ) -> Tuple[Optional[str], Optional[str]]:
        """Generate interactive chart and return URL and CSV filename."""
        try:
            # Create chart
            chart = Chart()
            chart.set(df)
            
            # Save CSV
            start_str = start_dt.strftime("%Y%m%d_%H%M")
            end_str = end_dt.strftime("%Y%m%d_%H%M")
            csv_filename = f"{pairs.replace('/', '_')}_{start_str}_to_{end_str}_chart_data.csv"
            df.to_csv(csv_filename)
            
            # Determine chart URL based on environment
            is_windows = platform.system() == 'Windows'
            chart_url = f"http://localhost:{self.settings.chart_server_port}"
            
            if is_windows:
                # For API usage, we don't auto-open the browser
                # The client can use the returned URL
                self.logger.info(f"Interactive chart available at: {chart_url}")
            
            return chart_url, csv_filename
            
        except Exception as e:
            self.logger.error(f"Failed to generate interactive chart: {e}")
            return None, None