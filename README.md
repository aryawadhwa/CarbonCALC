# CarbonCALC: Real-Time Carbon Footprint Monitoring and Predictive Reporting Cloud Solution

A comprehensive web-based platform for calculating, tracking, and reducing carbon footprints with personalized biosafety and sustainability recommendations.

## Features

### Core Functionality
- 👥 **Multi-User Support**: Individual, Institution, and Corporation user types
- 📊 **Carbon Footprint Calculator**: Comprehensive calculation across energy, transportation, waste, food, water, and corporate operations
- 🌱 **Personalized Recommendations**: AI-powered biosafety and sustainability feedback tailored to your footprint
- 📈 **Interactive Dashboard**: Real-time visualization of your carbon footprint trends
- 📋 **Historical Tracking**: Track your emissions over time and measure improvements

### Research-Grade Features
- 🤖 **Machine Learning Predictions**: Ensemble models (Random Forest + Gradient Boosting) for forecasting future carbon footprints
- 📡 **IoT Sensor Integration**: Real-time sensor network simulation for continuous emission monitoring
- 📊 **Comparative Benchmarking**: Statistical comparison against industry standards with percentile analysis
- 🔬 **Predictive Analytics**: Time-series forecasting with confidence intervals and trend analysis
- 📈 **Advanced Analytics**: Effect size calculations, performance ratings, and improvement potential quantification
- 📄 **Research Reports**: Comprehensive reports with statistical analysis and predictive insights

## Architecture

```
┌─────────────┐
│ IoT Sensors │──┐
└─────────────┘  │
                 ├──> [Cloud Backend] ──> [ML Models] ──> [Dashboard]
┌─────────────┐  │
│ Data Sources│──┘
└─────────────┘
```

## Tech Stack

- **Backend**: FastAPI (Python)
- **ML Framework**: Scikit-learn (CPU-optimized, no GPU required)
- **Database**: SQLite (production-ready for PostgreSQL)
- **Frontend**: HTML/CSS/JavaScript Dashboard
- **Cloud**: Free deployment ready (Render.com, Railway)
- **Compute**: CPU-only (works on free cloud hosting)

## Installation

1. Clone the repository or navigate to the project directory

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Initialize the database:
```bash
python init_db.py
```

4. Start the server:
```bash
python main.py
```
Or use uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

5. Open the web application:
- Navigate to `http://localhost:8000` in your browser
- Register a new account or login
- Start calculating your carbon footprint!

## Project Structure

```
CarbonCalc/
├── main.py                 # FastAPI backend application
├── models/                 # ML models directory
│   ├── carbon_predictor.py
│   └── trained_models/
├── iot/                    # IoT sensor simulation
│   └── sensor_simulator.py
├── database/               # Database models and setup
│   ├── models.py
│   └── database.py
├── api/                    # API routes
│   ├── routes.py
│   └── websocket.py
├── dashboard/              # Frontend dashboard
│   ├── index.html
│   └── static/
├── utils/                  # Utility functions
│   ├── data_processor.py
│   └── analytics.py
└── requirements.txt
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get access token
- `GET /api/auth/me` - Get current user information

### Carbon Footprint
- `POST /api/calculate` - Calculate carbon footprint
- `GET /api/entries` - Get user's carbon footprint entries
- `GET /api/entries/{id}` - Get specific entry
- `GET /api/recommendations` - Get sustainability recommendations

### Analytics & Research
- `GET /api/analytics/summary` - Get analytics summary
- `POST /api/predict` - Predict future carbon footprint using ML models
- `GET /api/benchmark/compare` - Compare against industry benchmarks
- `GET /api/research/report` - Generate comprehensive research report

### IoT Integration
- `GET /api/iot/sensors` - Get IoT sensor network readings
- `GET /api/iot/sensors/history` - Get historical IoT sensor data

## License

MIT License

