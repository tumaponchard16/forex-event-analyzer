````markdown
<!-- filepath: c:\Users\SK\Documents\chardiecode\historal-chart-events\README.md -->

# Historical Chart Events API - Production Grade FastAPI Application

A production-ready REST API for **tracking historical news events and analyzing forex market movements** during specific events like NFP, FOMC, GDP releases, and other major economic announcements.

## 🎯 **Primary Objective: News Event Impact Analysis**

This application is specifically designed to:

- **📰 Track Historical News Events** - Analyze market behavior during specific events (NFP, FOMC, CPI, etc.)
- **📊 Market Movement Analysis** - Study price action before, during, and after news releases
- **📈 Pattern Recognition** - Identify recurring market patterns around news events
- **🔍 Multi-Timeframe Analysis** - Examine impact across different timeframes
- **📋 Event Database** - Build a database of historical events and their market impact

## 🌟 Features

### 🎯 **News Event Tracking**

- **📰 Historical Event Analysis**: Track market movements during specific news events over multiple years
- **⏰ Pre/During/Post Analysis**: Analyze price action before, during, and after news releases
- **📊 Multi-Currency Impact**: Study how events affect multiple currency pairs simultaneously
- **🎯 Event-Specific Timeframes**: Configurable analysis windows (5min before/after, 1hr impact, etc.)
- **📈 Volatility Tracking**: Measure volatility spikes during news events
- **📋 Pattern Database**: Build historical patterns for recurring events (NFP, FOMC, etc.)

### 📊 **Market Impact Analysis**

- **🎲 Price Movement Metrics**: Calculate pips moved, percentage changes, high/low ranges
- **⚡ Volatility Analysis**: Measure pre-event vs post-event volatility
- **🕐 Reaction Time Analysis**: Track immediate vs delayed market reactions
- **📈 Trend Analysis**: Identify if events cause trend reversals or continuations
- **🎯 Support/Resistance Impact**: Analyze how news affects key technical levels
- **📊 Volume Analysis**: Study trading volume patterns during events

### 🗓️ **Event Examples Supported**

| Event Type                 | Frequency | Typical Impact      | Analysis Focus         |
| -------------------------- | --------- | ------------------- | ---------------------- |
| **NFP (Non-Farm Payroll)** | Monthly   | High (USD pairs)    | Employment data impact |
| **FOMC Rate Decision**     | 8x/year   | Very High (All USD) | Interest rate policy   |
| **CPI (Inflation Data)**   | Monthly   | High (Major pairs)  | Inflation expectations |
| **GDP Reports**            | Quarterly | Medium-High         | Economic growth        |
| **Central Bank Speeches**  | Weekly    | Variable            | Policy guidance        |
| **PMI Data**               | Monthly   | Medium              | Economic activity      |

### 🔧 **Production-Ready API**

- **FastAPI Framework**: Modern, fast web framework with automatic API docs
- **API Versioning**: Clean `/api/v1/` endpoint structure for future compatibility
- **Event Database**: Store and retrieve historical event data
- **Comprehensive Testing**: Unit, integration, and API tests with 80%+ coverage
- **Docker Support**: Containerized deployment with Docker Compose
- **Configuration Management**: Environment-based settings with validation
- **Structured Logging**: Detailed logging with configurable levels

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- Docker and Docker Compose (for containerized deployment)
- Internet connection (for downloading financial and news data)

### 🐳 **Docker Deployment (Recommended)**

#### **Quick Start Commands**

```bash
# Clone the repository
git clone <repository-url>
cd historal-chart-events

# Build and start the API
docker-compose up --build -d

# API will be available at http://localhost:8000
# API documentation at http://localhost:8000/docs
```

#### **📋 Complete Docker Commands Reference**

**🔨 Build Commands:**

```bash
# Build the Docker image
docker-compose build

# Build with no cache (clean build)
docker-compose build --no-cache

# Build and start services
docker-compose up --build

# Build with detailed progress output
docker-compose build --progress=plain
```

**🚀 Run Commands:**

```bash
# Start services in background (detached mode)
docker-compose up -d

# Start with build and logs
docker-compose up --build

# Start and follow logs
docker-compose up --build -d && docker-compose logs -f

# Start specific service only
docker-compose up forex-chart-api
```

**📊 Monitor & Debug Commands:**

```bash
# Check container status
docker-compose ps

# View logs (all services)
docker-compose logs

# Follow logs in real-time
docker-compose logs -f

# View logs for specific service
docker-compose logs forex-chart-api

# View last 50 log lines
docker-compose logs --tail=50 forex-chart-api

# Check container health
docker-compose exec forex-chart-api curl http://localhost:8000/api/v1/health
```

**🔧 Management Commands:**

```bash
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Stop and remove everything (containers, networks, images)
docker-compose down --rmi all --volumes --remove-orphans

# Restart services
docker-compose restart

# Restart specific service
docker-compose restart forex-chart-api

# Scale service (run multiple instances)
docker-compose up --scale forex-chart-api=3 -d
```

**🐚 Interactive Commands:**

```bash
# Execute command in running container
docker-compose exec forex-chart-api bash

# Run one-time command
docker-compose run --rm forex-chart-api python -c "print('Hello World')"

# Access Python shell in container
docker-compose exec forex-chart-api python

# Check installed packages
docker-compose exec forex-chart-api pip list

# Run tests inside container
docker-compose exec forex-chart-api pytest
```

**🔍 Troubleshooting Commands:**

```bash
# Check Docker system info
docker system df

# Clean up unused Docker resources
docker system prune

# Remove stopped containers
docker container prune

# Remove unused images
docker image prune

# View detailed container info
docker-compose exec forex-chart-api env

# Check port mappings
docker-compose port forex-chart-api 8000

# Inspect container configuration
docker inspect historal-chart-events-forex-chart-api
```

**⚡ Development Workflow:**

```bash
# Development mode with file watching
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build

# Update dependencies and rebuild
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Quick restart after code changes
docker-compose restart forex-chart-api

# View API documentation
curl http://localhost:8000/docs
# Or open in browser: http://localhost:8000/docs
```

#### **🎯 Common Use Cases:**

**First Time Setup:**

```bash
# Complete setup from scratch
git clone <repository-url>
cd historal-chart-events
docker-compose up --build -d
docker-compose logs -f
# Wait for "Application startup complete" message
# Open http://localhost:8000/docs
```

**Daily Development:**

```bash
# Start your development session
docker-compose up -d
docker-compose logs -f forex-chart-api

# After making code changes
docker-compose restart forex-chart-api

# End of day cleanup
docker-compose down
```

**Production Deployment:**

```bash
# Production build and deploy
docker-compose -f docker-compose.prod.yml up --build -d

# Health check
curl -f http://localhost:8000/api/v1/health || echo "Service not ready"

# Monitor production logs
docker-compose logs -f --tail=100 forex-chart-api
```

**Performance Testing:**

```bash
# Start with resource monitoring
docker-compose up -d
docker stats historal-chart-events-forex-chart-api

# Load test the API
curl -X POST "http://localhost:8000/api/v1/charts" \
  -H "Content-Type: application/json" \
  -d '{"pairs": "EUR/USD", "start_date_time": "2024-01-01", "end_date_time": "2024-12-31"}'
```

#### **📋 Expected Build Times:**

- **First build**: 5-15 minutes (downloads dependencies)
- **Subsequent builds**: 1-3 minutes (uses cache)
- **Code-only changes**: 30 seconds - 1 minute

#### **🔧 Environment Variables:**

```bash
# Create .env file for custom configuration
cat > .env << EOF
DEBUG=true
LOG_LEVEL=DEBUG
API_PORT=8001
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
EOF

# Start with custom environment
docker-compose up --build -d
```
````

### 📊 **Example: NFP Analysis**

```bash
# Analyze last 2 years of NFP events
curl -X POST "http://localhost:8000/api/v1/events/nfp-analysis" \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "NFP",
    "lookback_years": 2,
    "pairs": ["EUR/USD", "GBP/USD", "USD/JPY"],
    "analysis_window": {
      "pre_event_minutes": 30,
      "post_event_minutes": 120
    }
  }'
```

## 📊 API Documentation

### 🔗 **Event Analysis Endpoints**

#### **POST `/api/v1/events/analyze`** - Analyze Historical Event Impact

Analyze market movements during specific historical events.

**Request Body:**

```json
{
  "event_type": "NFP",
  "event_dates": [
    "2024-01-05 13:30:00",
    "2024-02-02 13:30:00",
    "2024-03-08 13:30:00"
  ],
  "pairs": ["EUR/USD", "GBP/USD", "USD/JPY"],
  "analysis_window": {
    "pre_event_minutes": 30,
    "post_event_minutes": 120
  },
  "interval": "1m"
}
```

**Response:**

```json
{
  "success": true,
  "event_analysis": {
    "event_type": "NFP",
    "total_events": 24,
    "analysis_period": "2023-01-01 to 2025-01-01",
    "pairs_analyzed": ["EUR/USD", "GBP/USD", "USD/JPY"],
    "summary_statistics": {
      "average_movement": {
        "EUR/USD": { "pips": 45.2, "percentage": 0.38 },
        "GBP/USD": { "pips": 52.8, "percentage": 0.42 },
        "USD/JPY": { "pips": 38.7, "percentage": 0.25 }
      },
      "volatility_increase": {
        "EUR/USD": "185%",
        "GBP/USD": "210%",
        "USD/JPY": "165%"
      },
      "direction_bias": {
        "bullish_events": 14,
        "bearish_events": 8,
        "neutral_events": 2
      }
    },
    "individual_events": [
      {
        "date": "2024-12-06 13:30:00",
        "actual": 227000,
        "forecast": 200000,
        "previous": 12000,
        "surprise": "positive",
        "market_reaction": {
          "EUR/USD": {
            "pre_event_price": 1.215,
            "immediate_reaction": -0.0025,
            "30min_movement": -0.0045,
            "2hour_movement": -0.0038,
            "max_volatility": 0.0067
          }
        }
      }
    ]
  }
}
```

#### **POST `/api/v1/events/nfp-tracker`** - NFP Historical Tracker

Specialized endpoint for Non-Farm Payroll analysis.

**Request Body:**

```json
{
  "lookback_years": 2,
  "pairs": ["EUR/USD", "GBP/USD", "USD/JPY", "USD/CHF"],
  "include_revisions": true,
  "analysis_type": "comprehensive"
}
```

#### **POST `/api/v1/events/fomc-tracker`** - FOMC Decision Tracker

Track Federal Reserve interest rate decisions and their market impact.

#### **GET `/api/v1/events/calendar`** - Economic Calendar

Get upcoming and historical economic events with market impact ratings.

#### **POST `/api/v1/charts/event-chart`** - Event-Specific Charts

Generate charts centered around specific news events.

**Request Body:**

```json
{
  "event_date": "2024-12-06 13:30:00",
  "event_type": "NFP",
  "pairs": "EUR/USD",
  "pre_event_hours": 2,
  "post_event_hours": 6,
  "interval": "1m",
  "mark_event_time": true
}
```

### 📊 **Event Types Supported**

| Code     | Event Name             | Release Time (EST)  | Frequency | Impact Level   |
| -------- | ---------------------- | ------------------- | --------- | -------------- |
| `NFP`    | Non-Farm Payroll       | 1st Fri 8:30 AM     | Monthly   | 🔴 High        |
| `FOMC`   | Fed Rate Decision      | Various 2:00 PM     | 8x/year   | 🔴 Very High   |
| `CPI`    | Consumer Price Index   | Mid-month 8:30 AM   | Monthly   | 🔴 High        |
| `GDP`    | Gross Domestic Product | End-month 8:30 AM   | Quarterly | 🟡 Medium-High |
| `JOLTS`  | Job Openings           | Monthly 10:00 AM    | Monthly   | 🟡 Medium      |
| `RETAIL` | Retail Sales           | Mid-month 8:30 AM   | Monthly   | 🟡 Medium      |
| `PMI`    | Manufacturing PMI      | 1st Bus Day 9:45 AM | Monthly   | 🟡 Medium      |

### 🎯 **Analysis Parameters**

| Parameter              | Description                     | Example | Default |
| ---------------------- | ------------------------------- | ------- | ------- |
| `lookback_years`       | Years to analyze back           | 2       | 1       |
| `pre_event_minutes`    | Minutes before event to analyze | 30      | 15      |
| `post_event_minutes`   | Minutes after event to track    | 120     | 60      |
| `include_revisions`    | Include revised data impact     | true    | false   |
| `volatility_threshold` | Minimum volatility to consider  | 0.5     | 0.3     |

## 📈 **NFP Analysis Use Case**

### **Objective: Track 2 Years of NFP Impact**

```python
import requests

# Analyze last 2 years of NFP events
nfp_analysis = requests.post("http://localhost:8000/api/v1/events/nfp-tracker", json={
    "lookback_years": 2,
    "pairs": ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD"],
    "analysis_window": {
        "pre_event_minutes": 30,   # 30 min before release
        "post_event_minutes": 180  # 3 hours after release
    },
    "include_revisions": True,
    "breakdown_by_surprise": True  # Group by positive/negative surprises
})

results = nfp_analysis.json()

# Key insights you'll get:
print(f"Analyzed {results['total_nfp_events']} NFP releases")
print(f"Average EUR/USD movement: {results['average_movement']['EUR/USD']} pips")
print(f"Strongest reaction pair: {results['most_volatile_pair']}")
print(f"Positive surprise win rate: {results['positive_surprise_accuracy']}%")
```

### **Expected NFP Analysis Output:**

```json
{
  "nfp_historical_analysis": {
    "period": "2023-01-06 to 2025-01-03",
    "total_events": 24,
    "summary": {
      "average_absolute_movement": {
        "EUR/USD": 42.3,
        "GBP/USD": 48.7,
        "USD/JPY": 35.2
      },
      "surprise_correlation": {
        "positive_surprises": {
          "count": 14,
          "avg_usd_strength": 38.5,
          "success_rate": "78%"
        },
        "negative_surprises": {
          "count": 8,
          "avg_usd_weakness": 31.2,
          "success_rate": "82%"
        }
      },
      "time_patterns": {
        "immediate_reaction": "85% within 1 minute",
        "peak_volatility": "Average 15-45 minutes post-release",
        "stabilization": "Average 2-3 hours post-release"
      }
    },
    "trading_insights": {
      "best_pairs_to_trade": ["EUR/USD", "GBP/USD"],
      "avoid_pairs": ["USD/CHF"],
      "optimal_entry": "2-5 minutes post-release",
      "risk_management": "Volatility 3x normal levels"
    }
  }
}
```

## 🧪 Example Analysis Workflows

### **1. Comprehensive NFP Study**

```bash
# Get all NFP events for last 2 years with detailed analysis
curl -X POST "http://localhost:8000/api/v1/events/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "NFP",
    "lookback_years": 2,
    "pairs": ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD"],
    "analysis_window": {
      "pre_event_minutes": 30,
      "post_event_minutes": 180
    },
    "breakdown_analysis": true,
    "include_surprise_factor": true
  }'
```

### **2. FOMC Rate Decision Impact**

```bash
# Analyze Fed rate decisions impact
curl -X POST "http://localhost:8000/api/v1/events/fomc-tracker" \
  -H "Content-Type: application/json" \
  -d '{
    "lookback_years": 3,
    "pairs": ["EUR/USD", "GBP/USD", "USD/JPY"],
    "include_dot_plot_meetings": true,
    "track_powell_speech": true
  }'
```

### **3. Multi-Event Correlation Study**

```bash
# Study correlation between different events
curl -X POST "http://localhost:8000/api/v1/events/correlation-analysis" \
  -H "Content-Type: application/json" \
  -d '{
    "primary_event": "NFP",
    "secondary_events": ["CPI", "RETAIL_SALES", "JOLTS"],
    "lookback_months": 18,
    "correlation_window_days": 7
  }'
```

## 📊 Chart Generation for Events

### **Event-Centered Charts**

```python
# Generate chart for specific NFP release
event_chart = requests.post("http://localhost:8000/api/v1/charts/event-chart", json={
    "event_date": "2024-12-06 13:30:00",  # Last NFP release
    "event_type": "NFP",
    "pairs": "EUR/USD",
    "pre_event_hours": 3,   # Show 3 hours before
    "post_event_hours": 6,  # Show 6 hours after
    "interval": "1m",
    "mark_event_time": True,  # Red vertical line at event time
    "show_volatility_bands": True
})
```

This will generate an interactive chart showing:

- ✅ 3 hours before NFP release
- ✅ Exact NFP release time marked
- ✅ 6 hours of post-NFP price action
- ✅ Volatility bands showing normal vs event volatility
- ✅ Key support/resistance levels

## 🛠️ Advanced Event Analysis Features

### **Pattern Recognition**

```json
{
  "pattern_analysis": {
    "pre_event_patterns": {
      "common_setup": "Range compression 30min before",
      "volume_pattern": "Decreasing volume pre-event",
      "fake_moves": "42% show false breakouts 5min before"
    },
    "post_event_patterns": {
      "initial_spike": "Average 15-45 pip spike within 1min",
      "retracement": "65% retrace 30-50% within 30min",
      "trend_continuation": "78% maintain direction after 2hrs"
    }
  }
}
```

### **Risk Management Insights**

```json
{
  "risk_insights": {
    "volatility_multiplier": 3.2,
    "stop_loss_recommendations": {
      "conservative": "50 pips",
      "moderate": "35 pips",
      "aggressive": "25 pips"
    },
    "optimal_position_sizing": "Reduce size by 60% during events"
  }
}
```

## 🎯 **Key Benefits for Traders**

1. **📊 Historical Perspective** - Understand how markets typically react to specific events
2. **🎯 Pattern Recognition** - Identify recurring patterns around news releases
3. **⚖️ Risk Management** - Better position sizing and stop-loss placement
4. **⏰ Timing Optimization** - Know optimal entry/exit times around events
5. **💰 Profit Opportunities** - Identify high-probability trading setups
6. **📈 Backtesting Data** - Historical data for strategy development

## 📁 Project Structure

```
historal-chart-events/
├── app/
│   ├── api/v1/
│   │   ├── charts.py          # Chart generation endpoints
│   │   ├── events.py          # Event analysis endpoints
│   │   └── calendar.py        # Economic calendar endpoints
│   ├── services/
│   │   ├── chart_service.py   # Chart generation
│   │   ├── event_service.py   # Event analysis logic
│   │   ├── nfp_service.py     # NFP-specific analysis
│   │   ├── fomc_service.py    # FOMC analysis
│   │   └── calendar_service.py # Economic calendar
│   ├── models/
│   │   ├── events.py          # Event-related models
│   │   ├── analysis.py        # Analysis result models
│   │   └── calendar.py        # Calendar models
│   └── data/
│       ├── economic_calendar.json  # Historical event dates
│       ├── nfp_releases.json      # NFP historical data
│       └── fomc_dates.json        # FOMC meeting dates
├── tests/
│   ├── events/                # Event analysis tests
│   ├── integration/           # Integration tests
│   └── fixtures/              # Test data fixtures
└── docs/
    ├── api_examples.md        # API usage examples
    ├── event_analysis_guide.md # Analysis methodology
    └── trading_insights.md    # Trading application guide
```

## 🔗 Dependencies

- **pandas**: Data manipulation and analysis
- **yfinance**: Yahoo Finance data download
- **lightweight-charts**: Interactive chart visualization
- **requests**: HTTP library for web requests
- **beautifulsoup4**: Web scraping for economic calendar
- **numpy**: Numerical computations for statistical analysis
- **scipy**: Advanced statistical analysis

---

**Happy Event Analysis! 📰📈**

```

```
