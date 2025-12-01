# Quick Start Guide

## Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

## Setup Steps

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Initialize Database**
   ```bash
   python init_db.py
   ```
   This creates the database tables and adds sample industry benchmarks.

3. **Start the Server**
   ```bash
   python main.py
   ```
   Or:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Access the Application**
   - Open your browser and navigate to: `http://localhost:8000`
   - Register a new account (choose Individual, Institution, or Corporation)
   - Login and start calculating your carbon footprint!

## Usage Guide

### For Individuals
1. Register as an "Individual" user
2. Fill in your monthly consumption data:
   - Energy usage (electricity, gas, heating oil)
   - Transportation (vehicle miles, public transport, flights)
   - Waste production and recycling rate
   - Food consumption (meat and vegetarian meals)
   - Water usage
3. Click "Calculate Carbon Footprint"
4. View your results and personalized recommendations

### For Institutions
1. Register as an "Institution" user
2. Provide your organization name
3. Fill in all individual fields plus:
   - Number of employees
   - Office space in square meters
   - Supply chain distance
4. Get institutional-level recommendations

### For Corporations
1. Register as a "Corporation" user
2. Provide your company name
3. Fill in comprehensive data including:
   - All institution fields
   - Manufacturing output (if applicable)
4. Receive corporate sustainability recommendations

## Features

- **Dashboard**: View your carbon footprint trends and statistics
- **Calculate**: Input your data and calculate your footprint
- **Recommendations**: Get personalized biosafety and sustainability recommendations
- **History**: Track your entries over time
- **Profile**: Manage your account information

## API Endpoints

- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get token
- `GET /api/auth/me` - Get current user info
- `POST /api/calculate` - Calculate carbon footprint
- `GET /api/entries` - Get user's entries
- `GET /api/recommendations` - Get recommendations
- `GET /api/analytics/summary` - Get analytics summary

## Troubleshooting

**Database errors**: Make sure you ran `python init_db.py` first
**Port already in use**: Change the port in `main.py` or use a different port with uvicorn
**Import errors**: Make sure all dependencies are installed with `pip install -r requirements.txt`

## Next Steps

- Calculate your baseline carbon footprint
- Review recommendations and implement changes
- Track your progress over time
- Share with your organization to improve sustainability

