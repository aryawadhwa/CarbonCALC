"""
IoT Sensor Data Simulator for Real-Time Carbon Emission Monitoring
Simulates industrial IoT sensors for continuous emission tracking
"""
import asyncio
import random
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import numpy as np


class IoTSensor:
    """Individual IoT sensor for carbon emission monitoring"""
    
    def __init__(self, sensor_id: str, sensor_type: str, location: str, baseline_emission: float):
        """
        Initialize IoT sensor
        Args:
            sensor_id: Unique sensor identifier
            sensor_type: Type of sensor (energy, manufacturing, transport, etc.)
            location: Physical location of sensor
            baseline_emission: Baseline emission value (kg CO2/hour)
        """
        self.sensor_id = sensor_id
        self.sensor_type = sensor_type
        self.location = location
        self.baseline_emission = baseline_emission
        self.current_emission = baseline_emission
        self.status = "active"
        self.last_update = datetime.utcnow()
    
    def read(self) -> Dict:
        """Read current sensor value with realistic variation"""
        # Add realistic noise and variation
        variation = random.uniform(-0.1, 0.1)  # ±10% variation
        # Add time-based patterns (e.g., lower emissions at night)
        hour_factor = 0.8 + 0.4 * (np.sin(2 * np.pi * datetime.utcnow().hour / 24) + 1) / 2
        
        self.current_emission = self.baseline_emission * (1 + variation) * hour_factor
        
        return {
            "sensor_id": self.sensor_id,
            "sensor_type": self.sensor_type,
            "location": self.location,
            "emission_kg_co2": round(self.current_emission, 2),
            "timestamp": datetime.utcnow().isoformat(),
            "status": self.status
        }


class SensorNetwork:
    """Network of IoT sensors for comprehensive emission monitoring"""
    
    def __init__(self):
        self.sensors: List[IoTSensor] = []
        self.readings_history: List[Dict] = []
        
    def add_sensor(self, sensor: IoTSensor):
        """Add sensor to network"""
        self.sensors.append(sensor)
    
    def create_default_network(self, user_type: str = "corporation"):
        """Create a default sensor network based on user type"""
        self.sensors.clear()
        
        if user_type == "corporation":
            # Manufacturing sensors
            for i in range(5):
                self.add_sensor(IoTSensor(
                    f"MFG-{i+1}",
                    "manufacturing",
                    f"Production Line {i+1}",
                    baseline_emission=random.uniform(50, 200)
                ))
            
            # Energy sensors
            for i in range(3):
                self.add_sensor(IoTSensor(
                    f"ENERGY-{i+1}",
                    "energy",
                    f"Building {i+1}",
                    baseline_emission=random.uniform(30, 100)
                ))
            
            # Transport sensors
            for i in range(2):
                self.add_sensor(IoTSensor(
                    f"TRANS-{i+1}",
                    "transportation",
                    f"Fleet {i+1}",
                    baseline_emission=random.uniform(20, 80)
                ))
        
        elif user_type == "institution":
            # Building energy sensors
            for i in range(3):
                self.add_sensor(IoTSensor(
                    f"BLDG-{i+1}",
                    "energy",
                    f"Building {i+1}",
                    baseline_emission=random.uniform(20, 60)
                ))
            
            # HVAC sensors
            self.add_sensor(IoTSensor(
                "HVAC-1",
                "hvac",
                "Central System",
                baseline_emission=random.uniform(15, 40)
            ))
        
        else:  # individual
            # Home energy sensor
            self.add_sensor(IoTSensor(
                "HOME-1",
                "energy",
                "Residence",
                baseline_emission=random.uniform(5, 15)
            ))
    
    def read_all(self) -> List[Dict]:
        """Read all sensors in network"""
        readings = []
        total_emission = 0
        
        for sensor in self.sensors:
            if sensor.status == "active":
                reading = sensor.read()
                readings.append(reading)
                total_emission += reading["emission_kg_co2"]
        
        # Aggregate reading
        aggregate = {
            "timestamp": datetime.utcnow().isoformat(),
            "total_emission_kg_co2": round(total_emission, 2),
            "sensor_count": len(self.sensors),
            "active_sensors": len([s for s in self.sensors if s.status == "active"]),
            "readings": readings
        }
        
        self.readings_history.append(aggregate)
        
        # Keep only last 1000 readings
        if len(self.readings_history) > 1000:
            self.readings_history = self.readings_history[-1000:]
        
        return aggregate
    
    def get_historical_summary(self, hours: int = 24) -> Dict:
        """Get summary statistics for historical readings"""
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        
        relevant_readings = [
            r for r in self.readings_history
            if datetime.fromisoformat(r["timestamp"]) >= cutoff_time
        ]
        
        if not relevant_readings:
            return {"error": "No data available"}
        
        emissions = [r["total_emission_kg_co2"] for r in relevant_readings]
        
        return {
            "period_hours": hours,
            "data_points": len(relevant_readings),
            "total_emission_kg_co2": round(sum(emissions), 2),
            "average_hourly_emission": round(np.mean(emissions), 2),
            "peak_emission": round(max(emissions), 2),
            "min_emission": round(min(emissions), 2),
            "std_deviation": round(np.std(emissions), 2)
        }
    
    async def stream_readings(self, interval_seconds: int = 5, callback=None):
        """Continuously stream sensor readings"""
        while True:
            reading = self.read_all()
            if callback:
                await callback(reading)
            await asyncio.sleep(interval_seconds)


# Global sensor network instance
_sensor_networks: Dict[str, SensorNetwork] = {}


def get_sensor_network(user_id: str, user_type: str) -> SensorNetwork:
    """Get or create sensor network for user"""
    if user_id not in _sensor_networks:
        network = SensorNetwork()
        network.create_default_network(user_type)
        _sensor_networks[user_id] = network
    return _sensor_networks[user_id]

