"""
Database models for Carbon Footprint Monitoring System
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.database import Base
import enum


class UserType(str, enum.Enum):
    INDIVIDUAL = "individual"
    INSTITUTION = "institution"
    CORPORATION = "corporation"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    user_type = Column(SQLEnum(UserType), default=UserType.INDIVIDUAL)
    organization_name = Column(String, nullable=True)  # For institutions/corporations
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    carbon_entries = relationship("CarbonEntry", back_populates="user")
    recommendations = relationship("Recommendation", back_populates="user")


class CarbonEntry(Base):
    __tablename__ = "carbon_entries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Energy Consumption (kWh)
    electricity_usage = Column(Float, default=0)
    gas_usage = Column(Float, default=0)
    heating_oil = Column(Float, default=0)
    
    # Transportation (km or miles)
    vehicle_miles = Column(Float, default=0)
    public_transport_km = Column(Float, default=0)
    flights_km = Column(Float, default=0)
    
    # Waste Management (kg)
    waste_produced = Column(Float, default=0)
    recycling_rate = Column(Float, default=0)  # percentage
    
    # Food & Lifestyle
    meat_consumption = Column(Float, default=0)  # kg per month
    vegetarian_meals = Column(Float, default=0)  # per month
    
    # Water Usage (liters)
    water_usage = Column(Float, default=0)
    
    # For Corporations/Institutions
    employee_count = Column(Integer, default=1)
    office_space_sqm = Column(Float, default=0)
    manufacturing_output = Column(Float, default=0)  # tons
    supply_chain_distance = Column(Float, default=0)  # km
    
    # Calculated Values
    total_carbon_footprint = Column(Float, default=0)  # CO2 equivalent in kg
    category_breakdown = Column(Text)  # JSON string
    
    # Metadata
    entry_date = Column(DateTime(timezone=True), server_default=func.now())
    period_start = Column(DateTime(timezone=True))
    period_end = Column(DateTime(timezone=True))
    notes = Column(Text, nullable=True)

    # Relationships
    user = relationship("User", back_populates="carbon_entries")
    recommendations = relationship("Recommendation", back_populates="carbon_entry")


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    carbon_entry_id = Column(Integer, ForeignKey("carbon_entries.id"), nullable=True)
    
    category = Column(String)  # energy, transportation, waste, food, water, etc.
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    impact_rating = Column(Integer)  # 1-5, how much impact this change will have
    difficulty = Column(String)  # easy, medium, hard
    estimated_reduction = Column(Float)  # kg CO2 reduction
    cost_estimate = Column(String, nullable=True)  # free, low, medium, high
    priority = Column(Integer, default=0)  # Higher = more important
    
    is_implemented = Column(Integer, default=0)  # 0 = not implemented, 1 = implemented
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="recommendations")
    carbon_entry = relationship("CarbonEntry", back_populates="recommendations")


class IndustryBenchmark(Base):
    __tablename__ = "industry_benchmarks"

    id = Column(Integer, primary_key=True, index=True)
    industry_type = Column(String, nullable=False)  # tech, manufacturing, healthcare, etc.
    user_type = Column(SQLEnum(UserType), nullable=False)
    average_carbon_per_person = Column(Float)  # kg CO2 per person
    average_carbon_total = Column(Float)  # kg CO2 total
    benchmark_year = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

