"""
API Routes for CarbonCALC - Carbon Footprint Monitoring System
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import desc
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime, timedelta
import json

from database.database import get_db
from database.models import User, CarbonEntry, Recommendation, UserType, IndustryBenchmark
from auth.auth import (
    get_current_active_user,
    get_password_hash,
    verify_password,
    create_access_token,
    require_user_type
)
from utils.carbon_calculator import CarbonCalculator
from utils.recommendations import RecommendationEngine
from utils.benchmarking import BenchmarkAnalyzer
from ml_models.predictor import CarbonFootprintPredictor
from iot.sensor_simulator import get_sensor_network

router = APIRouter()


# Pydantic models for request/response
class UserRegister(BaseModel):
    email: EmailStr
    username: str
    password: str
    full_name: str
    user_type: UserType
    organization_name: Optional[str] = None


class UserLogin(BaseModel):
    username: str
    password: str


class CarbonEntryInput(BaseModel):
    electricity_usage: float = 0
    gas_usage: float = 0
    heating_oil: float = 0
    vehicle_miles: float = 0
    public_transport_km: float = 0
    flights_km: float = 0
    waste_produced: float = 0
    recycling_rate: float = 0
    meat_consumption: float = 0
    vegetarian_meals: float = 0
    water_usage: float = 0
    employee_count: int = 1
    office_space_sqm: float = 0
    manufacturing_output: float = 0
    supply_chain_distance: float = 0
    period_start: Optional[datetime] = None
    period_end: Optional[datetime] = None
    notes: Optional[str] = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict


# Authentication Routes
@router.post("/auth/register", response_model=dict)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if user exists
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
        user_type=user_data.user_type,
        organization_name=user_data.organization_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return {
        "message": "User registered successfully",
        "user_id": db_user.id,
        "username": db_user.username
    }


@router.post("/auth/login", response_model=TokenResponse)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Login and get access token"""
    user = db.query(User).filter(User.username == credentials.username).first()
    
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    if user.is_active == 0:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    access_token = create_access_token(data={"sub": user.id})
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user={
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "user_type": user.user_type.value,
            "organization_name": user.organization_name
        }
    )


@router.get("/auth/me", response_model=dict)
async def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    """Get current user information"""
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "user_type": current_user.user_type.value,
        "organization_name": current_user.organization_name
    }


# Carbon Footprint Routes
@router.post("/calculate", response_model=dict)
async def calculate_carbon_footprint(
    entry_data: CarbonEntryInput,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Calculate carbon footprint from input data"""
    # Prepare data for calculator
    calc_data = entry_data.dict()
    calc_data["user_type"] = current_user.user_type.value
    
    # Calculate footprint
    footprint_breakdown = CarbonCalculator.calculate_total_footprint(calc_data)
    
    # Create database entry
    db_entry = CarbonEntry(
        user_id=current_user.id,
        **entry_data.dict(),
        total_carbon_footprint=footprint_breakdown["total"],
        category_breakdown=json.dumps(footprint_breakdown),
        period_start=entry_data.period_start or datetime.utcnow() - timedelta(days=30),
        period_end=entry_data.period_end or datetime.utcnow()
    )
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    
    # Generate recommendations
    recommendations = RecommendationEngine.generate_recommendations(
        footprint_breakdown,
        current_user.user_type
    )
    
    # Save recommendations to database
    for rec in recommendations:
        db_rec = Recommendation(
            user_id=current_user.id,
            carbon_entry_id=db_entry.id,
            category=rec.get("category", "general"),
            title=rec.get("title", ""),
            description=rec.get("description", ""),
            impact_rating=rec.get("impact_rating", 0),
            difficulty=rec.get("difficulty", "easy"),
            estimated_reduction=rec.get("estimated_reduction", 0),
            cost_estimate=rec.get("cost_estimate", "N/A"),
            priority=rec.get("priority", 0)
        )
        db.add(db_rec)
    db.commit()
    
    return {
        "entry_id": db_entry.id,
        "footprint": footprint_breakdown,
        "recommendations": recommendations
    }


@router.get("/entries", response_model=List[dict])
async def get_user_entries(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    limit: int = 10
):
    """Get user's carbon footprint entries"""
    entries = db.query(CarbonEntry).filter(
        CarbonEntry.user_id == current_user.id
    ).order_by(desc(CarbonEntry.entry_date)).limit(limit).all()
    
    return [
        {
            "id": entry.id,
            "total_carbon_footprint": entry.total_carbon_footprint,
            "category_breakdown": json.loads(entry.category_breakdown) if entry.category_breakdown else {},
            "entry_date": entry.entry_date.isoformat() if entry.entry_date else None,
            "period_start": entry.period_start.isoformat() if entry.period_start else None,
            "period_end": entry.period_end.isoformat() if entry.period_end else None,
            "notes": entry.notes
        }
        for entry in entries
    ]


@router.get("/entries/{entry_id}", response_model=dict)
async def get_entry(
    entry_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get specific carbon footprint entry"""
    entry = db.query(CarbonEntry).filter(
        CarbonEntry.id == entry_id,
        CarbonEntry.user_id == current_user.id
    ).first()
    
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entry not found"
        )
    
    recommendations = db.query(Recommendation).filter(
        Recommendation.carbon_entry_id == entry_id
    ).all()
    
    return {
        "id": entry.id,
        "total_carbon_footprint": entry.total_carbon_footprint,
        "category_breakdown": json.loads(entry.category_breakdown) if entry.category_breakdown else {},
        "entry_date": entry.entry_date.isoformat() if entry.entry_date else None,
        "recommendations": [
            {
                "id": rec.id,
                "category": rec.category,
                "title": rec.title,
                "description": rec.description,
                "impact_rating": rec.impact_rating,
                "difficulty": rec.difficulty,
                "estimated_reduction": rec.estimated_reduction,
                "cost_estimate": rec.cost_estimate,
                "priority": rec.priority
            }
            for rec in recommendations
        ]
    }


@router.get("/recommendations", response_model=List[dict])
async def get_recommendations(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get user's recommendations"""
    recommendations = db.query(Recommendation).filter(
        Recommendation.user_id == current_user.id,
        Recommendation.is_implemented == 0
    ).order_by(desc(Recommendation.priority)).all()
    
    return [
        {
            "id": rec.id,
            "category": rec.category,
            "title": rec.title,
            "description": rec.description,
            "impact_rating": rec.impact_rating,
            "difficulty": rec.difficulty,
            "estimated_reduction": rec.estimated_reduction,
            "cost_estimate": rec.cost_estimate,
            "priority": rec.priority,
            "created_at": rec.created_at.isoformat() if rec.created_at else None
        }
        for rec in recommendations
    ]


@router.get("/analytics/summary", response_model=dict)
async def get_analytics_summary(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get analytics summary for user"""
    entries = db.query(CarbonEntry).filter(
        CarbonEntry.user_id == current_user.id
    ).order_by(desc(CarbonEntry.entry_date)).limit(12).all()
    
    if not entries:
        return {
            "total_entries": 0,
            "average_footprint": 0,
            "trend": "no_data"
        }
    
    total_footprints = [e.total_carbon_footprint for e in entries]
    avg_footprint = sum(total_footprints) / len(total_footprints)
    
    # Calculate trend
    if len(entries) >= 2:
        recent = entries[0].total_carbon_footprint
        previous = entries[1].total_carbon_footprint
        if recent < previous * 0.95:
            trend = "decreasing"
        elif recent > previous * 1.05:
            trend = "increasing"
        else:
            trend = "stable"
    else:
        trend = "no_trend"
    
    return {
        "total_entries": len(entries),
        "average_footprint": round(avg_footprint, 2),
        "latest_footprint": round(entries[0].total_carbon_footprint, 2),
        "trend": trend
    }


# Research-grade API endpoints
@router.post("/predict", response_model=dict)
async def predict_footprint(
    forecast_periods: int = 12,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Predict future carbon footprint using ML models"""
    entries = db.query(CarbonEntry).filter(
        CarbonEntry.user_id == current_user.id
    ).order_by(desc(CarbonEntry.entry_date)).limit(24).all()
    
    if len(entries) < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient historical data for prediction. Need at least 2 entries."
        )
    
    # Convert to dict format
    historical_data = [
        {
            "entry_date": e.entry_date.isoformat() if e.entry_date else None,
            "total_carbon_footprint": e.total_carbon_footprint,
            "category_breakdown": json.loads(e.category_breakdown) if e.category_breakdown else {}
        }
        for e in reversed(entries)  # Reverse to chronological order
    ]
    
    # Create and train predictor (optimized for CPU, no GPU needed)
    # Uses lightweight ensemble model that runs efficiently on standard hardware
    predictor = CarbonFootprintPredictor(model_type="ensemble")
    training_metrics = predictor.train(historical_data)
    
    # Generate predictions
    predictions = predictor.predict(historical_data, forecast_periods=forecast_periods)
    
    return {
        "predictions": predictions,
        "model_metrics": training_metrics,
        "methodology": "ensemble_random_forest_gradient_boosting"
    }


@router.get("/iot/sensors", response_model=dict)
async def get_iot_sensors(
    current_user: User = Depends(get_current_active_user)
):
    """Get IoT sensor network status and readings"""
    sensor_network = get_sensor_network(str(current_user.id), current_user.user_type.value)
    reading = sensor_network.read_all()
    return reading


@router.get("/iot/sensors/history", response_model=dict)
async def get_iot_history(
    hours: int = 24,
    current_user: User = Depends(get_current_active_user)
):
    """Get historical IoT sensor data"""
    sensor_network = get_sensor_network(str(current_user.id), current_user.user_type.value)
    summary = sensor_network.get_historical_summary(hours=hours)
    return summary


@router.get("/benchmark/compare", response_model=dict)
async def compare_with_benchmark(
    entry_id: Optional[int] = None,
    industry_type: Optional[str] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Compare carbon footprint against industry benchmarks"""
    if entry_id:
        entry = db.query(CarbonEntry).filter(
            CarbonEntry.id == entry_id,
            CarbonEntry.user_id == current_user.id
        ).first()
        if not entry:
            raise HTTPException(status_code=404, detail="Entry not found")
        footprint = entry.total_carbon_footprint
        employee_count = entry.employee_count or 1
    else:
        # Use latest entry
        entry = db.query(CarbonEntry).filter(
            CarbonEntry.user_id == current_user.id
        ).order_by(desc(CarbonEntry.entry_date)).first()
        if not entry:
            raise HTTPException(status_code=404, detail="No entries found")
        footprint = entry.total_carbon_footprint
        employee_count = entry.employee_count or 1
    
    comparison = BenchmarkAnalyzer.compare_with_benchmark(
        footprint,
        current_user.user_type,
        employee_count,
        db,
        industry_type
    )
    
    return comparison


@router.get("/research/report", response_model=dict)
async def get_research_report(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Generate comprehensive research report"""
    # Get user entries
    entries = db.query(CarbonEntry).filter(
        CarbonEntry.user_id == current_user.id
    ).order_by(desc(CarbonEntry.entry_date)).all()
    
    if not entries:
        raise HTTPException(status_code=404, detail="No data available for report")
    
    entries_dict = [
        {
            "entry_date": e.entry_date.isoformat() if e.entry_date else None,
            "total_carbon_footprint": e.total_carbon_footprint,
            "employee_count": e.employee_count or 1
        }
        for e in entries
    ]
    
    # Get benchmarks
    benchmarks = db.query(IndustryBenchmark).filter(
        IndustryBenchmark.user_type == current_user.user_type
    ).all()
    
    # Generate comparative report
    comparative_report = BenchmarkAnalyzer.generate_comparative_report(
        entries_dict,
        benchmarks,
        current_user.user_type
    )
    
    # Add predictions if enough data
    predictions_data = None
    if len(entries) >= 2:
        historical_data = [
            {
                "entry_date": e.entry_date.isoformat() if e.entry_date else None,
                "total_carbon_footprint": e.total_carbon_footprint,
                "category_breakdown": json.loads(e.category_breakdown) if e.category_breakdown else {}
            }
            for e in reversed(entries)
        ]
        predictor = CarbonFootprintPredictor(model_type="ensemble")
        predictor.train(historical_data)
        predictions_data = predictor.predict(historical_data, forecast_periods=12)
    
    return {
        "user_info": {
            "user_type": current_user.user_type.value,
            "organization": current_user.organization_name,
            "total_entries": len(entries)
        },
        "comparative_analysis": comparative_report,
        "predictions": predictions_data,
        "research_metadata": {
            "report_generated": datetime.utcnow().isoformat(),
            "methodology": "ml_ensemble_prediction_with_benchmark_analysis",
            "data_points": len(entries)
        }
    }

