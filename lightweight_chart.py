# chart.py
from datetime import datetime, timedelta
import yfinance as yf
from lightweight_charts import Chart
import pandas as pd

def lightweight_chart(pairs: str, start_date_time: str, end_date_time: str,
                      interval: str = "5m"):
    """
    Draw a candlestick chart for `pairs` between start and end datetime.
    All candles in the specified range will be visible when the chart opens.
    Example: lightweight_chart("EUR/USD", "2025-08-25 10:00 AM", "2025-08-26 10:00 AM")

    Args:
        pairs: "EUR/USD"
        start_date_time: "YYYY-MM-DD HH:MM AM/PM" or "YYYY-MM-DD HH:MM"
        end_date_time: "YYYY-MM-DD HH:MM AM/PM" or "YYYY-MM-DD HH:MM"
        interval: yfinance interval (e.g., "1m","5m","15m","1h","1d")
    """
    # 1) parse the start and end datetimes (assumes system local timezone)
    def parse_datetime(date_str):
        """Parse datetime string in multiple formats"""
        formats = [
            "%Y-%m-%d %I:%M %p",    # 2025-08-25 10:00 AM
            "%Y-%m-%d %H:%M",       # 2025-08-25 10:00 (24-hour)
            "%Y-%m-%d %I:%M%p",     # 2025-08-25 10:00AM (no space)
        ]
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        raise ValueError(f"Unable to parse datetime: {date_str}. Use format like '2025-08-25 10:00 AM' or '2025-08-25 10:00'")
    
    start_dt = parse_datetime(start_date_time)
    end_dt = parse_datetime(end_date_time)

    # 2) prepare candidate yahoo tickers to try
    pair_clean = pairs.upper().replace(' ', '')
    base, quote = pair_clean.split('/')
    candidates = [
        pair_clean.replace('/', '') + '=X',  # EURUSD=X
        base + quote + '=X',                 # EURUSD=X (same)
        quote + base + '=X',                 # USDEUR=X (fallback)
        quote + '=X'                         # sometimes JPY=X works for USD/JPY
    ]

    start = start_dt
    end = end_dt

    df = None
    used_symbol = None
    # 3) try candidates until we get data
    for sym in candidates:
        try:
            df_try = yf.download(sym, start=start, end=end, interval=interval, progress=False, auto_adjust=True)
            # Check if df_try is empty or None
            if df_try is not None and isinstance(df_try, pd.DataFrame) and not df_try.empty:
                df = df_try
                used_symbol = sym
                break
        except Exception as e:
            print(f"Failed to download {sym}: {e}")
            continue

    if df is None or df.empty:
        raise RuntimeError(f"No data found for {pairs}. Tried: {candidates}")

    # 4) prepare data for lightweight-charts (remove duplicate times)
    df = df[~df.index.duplicated(keep='first')]

    data = []
    for idx, row in df.iterrows():
        # idx is a pandas.Timestamp — .timestamp() gives epoch seconds
        ts = int(idx.timestamp())
        
        # Handle both Series and scalar values
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
            data.append({
                "time": ts,
                "open": open_val,
                "high": high_val,
                "low": low_val,
                "close": close_val,
            })

    # 5) create chart and set data
    # Convert data to DataFrame first
    chart_df = pd.DataFrame(data)
    if chart_df.empty:
        raise RuntimeError("No valid data points created")
        
    chart_df['time'] = pd.to_datetime(chart_df['time'], unit='s')
    chart_df.set_index('time', inplace=True)
    
    # Create chart with specific configuration for fitting content
    chart = Chart()
    
    # Set the DataFrame data
    chart.set(chart_df)
    
    # Don't set any visible range - let the chart auto-fit all data
    print(f"📏 Chart will display {len(chart_df)} candles automatically")

    # 7) show chart (this opens a browser tab with an interactive chart)
    print(f"📊 Chart created successfully for {pairs}")
    print(f"📈 Data points: {len(chart_df)}")
    print(f"📅 Date range: {chart_df.index.min()} to {chart_df.index.max()}")
    print(f"💰 Price range: ${chart_df['low'].min():.5f} - ${chart_df['high'].max():.5f}")
    
    # Save chart data to CSV for reference
    start_str = start_dt.strftime("%Y%m%d_%H%M")
    end_str = end_dt.strftime("%Y%m%d_%H%M")
    csv_filename = f"{pairs.replace('/', '_')}_{start_str}_to_{end_str}_chart_data.csv"
    chart_df.to_csv(csv_filename)
    print(f"💾 Chart data saved to: {csv_filename}")
    
    # Check environment and show chart
    import os
    import platform
    
    # Detect Windows vs WSL vs Linux
    is_windows = platform.system() == 'Windows'
    is_wsl = 'microsoft' in platform.uname().release.lower() if hasattr(platform.uname(), 'release') else False
    display = os.environ.get('DISPLAY')
    wayland_display = os.environ.get('WAYLAND_DISPLAY')
    
    print("🌐 Opening interactive chart...")
    
    try:
        if is_windows:
            # Running on native Windows - chart should open in default browser
            print("🖥️  Running on Windows - opening chart in browser...")
            try:
                # Try to show the chart with blocking first
                chart.show(block=False)
                print("✅ Chart server started!")
                print("🌐 If chart didn't open automatically, try manually opening:")
                print("   http://localhost:5500 in your web browser")
                
                # Give the chart time to load, then try to fit content
                import time
                print("⏳ Waiting for chart to load...")
                time.sleep(2)
                
                # Try to fit content after the chart has loaded
                try:
                    chart.fit_content()
                    print("🎯 Auto-fitted all candles to screen!")
                except Exception as fit_error:
                    print(f"ℹ️  Auto-fit not available: {fit_error}")
                    print("💡 Tip: Press 'Ctrl + A' or use mouse wheel to zoom out and see all candles")
                
                # Keep the script running so the chart server stays active
                input("\n📊 Chart is running! Press Enter to close the chart server...")
                
            except Exception as browser_error:
                print(f"⚠️  Browser auto-open failed: {browser_error}")
                print("🔧 Trying alternative method...")
                
                # Try alternative approach
                import webbrowser
                chart.show(block=False)
                
                # Give server time to start
                import time
                time.sleep(1)
                
                # Try to open browser manually
                try:
                    webbrowser.open('http://localhost:5500')
                    print("✅ Opened chart in browser manually!")
                except:
                    print("💡 Please manually open: http://localhost:5500")
                
                input("\n📊 Chart is running! Press Enter to close the chart server...")
            
        elif is_wsl or display or wayland_display:
            # Running in WSL or Linux with display
            if is_wsl:
                print("🖥️  WSL detected - attempting to open chart...")
            else:
                print(f"🖥️  Linux display detected - DISPLAY: {display}, WAYLAND: {wayland_display}")
            
            chart.show(block=False)
            print("✅ Chart should now be opening!")
            
            # Give it a moment to launch
            import time
            time.sleep(2)
            
        else:
            # Headless environment
            print("🖥️  Headless environment detected")
            print("💡 Chart data is available in the CSV file above")
            print("📋 To view chart interactively, run this script on a system with GUI support")
            return chart_df
            
    except Exception as e:
        print(f"⚠️  Could not open chart display: {e}")
        print("� Chart data is available in the CSV file above")
        
        # Provide troubleshooting based on environment
        if is_windows:
            print("\n🛠️  Windows troubleshooting:")
            print("   1. Make sure you have a default web browser set")
            print("   2. Try running as administrator if needed")
            print("   3. Check if any firewall is blocking the local server")
        elif is_wsl:
            print("\n🛠️  WSL troubleshooting:")
            print("   1. Make sure Windows is updated")
            print("   2. Update WSL: wsl --update")
            print("   3. Restart WSL: wsl --shutdown then reopen")
        else:
            print("\n�️  Linux troubleshooting:")
            print("   1. Make sure DISPLAY variable is set correctly")
            print("   2. Check if X11 forwarding is enabled for SSH sessions")
            print("   3. Install a web browser if not available")
    
    return chart_df

if __name__ == "__main__":
    # example: change these to the pair/date/time you want
    # lightweight_chart(pairs="EUR/USD", start_date_time="2025-08-25 10:00 AM", end_date_time="2025-08-26 10:00 AM")
    lightweight_chart("GBP/USD", "2025-08-20 08:00 AM", "2025-08-21 08:00 AM", interval="15m")