"""
Carbon Footprint Calculation Engine
Calculates CO2 equivalent emissions based on various inputs
"""
from typing import Dict, Any
import json


class CarbonCalculator:
    """
    Carbon footprint calculator using standard emission factors
    All calculations return CO2 equivalent in kg
    """
    
    # Emission factors (kg CO2 per unit)
    EMISSION_FACTORS = {
        # Energy (per kWh)
        "electricity_grid": 0.5,  # Average grid mix
        "electricity_renewable": 0.05,
        "natural_gas": 0.2,  # per kWh
        "heating_oil": 0.3,  # per kWh
        "coal": 0.9,  # per kWh
        
        # Transportation (per km)
        "car_gasoline": 0.2,  # average car
        "car_electric": 0.05,
        "public_transport": 0.1,
        "flight_domestic": 0.25,
        "flight_international": 0.3,
        
        # Waste (per kg)
        "waste_landfill": 2.0,  # methane equivalent
        "waste_recycled": 0.3,
        
        # Food (per kg)
        "meat_beef": 27.0,
        "meat_pork": 12.0,
        "meat_chicken": 6.5,
        "vegetarian_meal": 2.0,
        
        # Water (per liter, including treatment and heating)
        "water_usage": 0.0003,  # very small but measurable
        
        # Corporate/Institutional
        "office_space": 0.05,  # per sqm per year
        "employee_commute": 2.0,  # per employee per day
    }
    
    @staticmethod
    def calculate_energy_emissions(electricity: float, gas: float, heating_oil: float) -> float:
        """Calculate emissions from energy consumption"""
        electricity_emissions = electricity * CarbonCalculator.EMISSION_FACTORS["electricity_grid"]
        gas_emissions = gas * CarbonCalculator.EMISSION_FACTORS["natural_gas"]
        oil_emissions = heating_oil * CarbonCalculator.EMISSION_FACTORS["heating_oil"]
        
        return electricity_emissions + gas_emissions + oil_emissions
    
    @staticmethod
    def calculate_transportation_emissions(
        vehicle_miles: float,
        public_transport_km: float,
        flights_km: float
    ) -> float:
        """Calculate emissions from transportation"""
        # Convert miles to km if needed (assuming km input)
        vehicle_emissions = vehicle_miles * CarbonCalculator.EMISSION_FACTORS["car_gasoline"]
        public_transport_emissions = public_transport_km * CarbonCalculator.EMISSION_FACTORS["public_transport"]
        flight_emissions = flights_km * CarbonCalculator.EMISSION_FACTORS["flight_domestic"]
        
        return vehicle_emissions + public_transport_emissions + flight_emissions
    
    @staticmethod
    def calculate_waste_emissions(waste_produced: float, recycling_rate: float) -> float:
        """Calculate emissions from waste management"""
        recycled_waste = waste_produced * (recycling_rate / 100)
        landfill_waste = waste_produced * (1 - recycling_rate / 100)
        
        recycled_emissions = recycled_waste * CarbonCalculator.EMISSION_FACTORS["waste_recycled"]
        landfill_emissions = landfill_waste * CarbonCalculator.EMISSION_FACTORS["waste_landfill"]
        
        return recycled_emissions + landfill_emissions
    
    @staticmethod
    def calculate_food_emissions(meat_consumption: float, vegetarian_meals: float) -> float:
        """Calculate emissions from food consumption"""
        # Average meat emissions (mix of beef, pork, chicken)
        avg_meat_emission = (
            CarbonCalculator.EMISSION_FACTORS["meat_beef"] * 0.3 +
            CarbonCalculator.EMISSION_FACTORS["meat_pork"] * 0.3 +
            CarbonCalculator.EMISSION_FACTORS["meat_chicken"] * 0.4
        )
        meat_emissions = meat_consumption * avg_meat_emission
        vegetarian_emissions = vegetarian_meals * CarbonCalculator.EMISSION_FACTORS["vegetarian_meal"]
        
        return meat_emissions + vegetarian_emissions
    
    @staticmethod
    def calculate_water_emissions(water_usage: float) -> float:
        """Calculate emissions from water usage"""
        return water_usage * CarbonCalculator.EMISSION_FACTORS["water_usage"]
    
    @staticmethod
    def calculate_corporate_emissions(
        employee_count: int,
        office_space_sqm: float,
        manufacturing_output: float,
        supply_chain_distance: float
    ) -> float:
        """Calculate additional emissions for corporations/institutions"""
        office_emissions = office_space_sqm * CarbonCalculator.EMISSION_FACTORS["office_space"]
        commute_emissions = employee_count * CarbonCalculator.EMISSION_FACTORS["employee_commute"] * 250  # working days
        manufacturing_emissions = manufacturing_output * 1000  # rough estimate: 1 ton = 1000 kg CO2
        supply_chain_emissions = supply_chain_distance * 0.15  # average freight emission
        
        return office_emissions + commute_emissions + manufacturing_emissions + supply_chain_emissions
    
    @staticmethod
    def calculate_total_footprint(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate total carbon footprint from all inputs
        Returns breakdown by category and total
        """
        # Energy
        energy_emissions = CarbonCalculator.calculate_energy_emissions(
            data.get("electricity_usage", 0),
            data.get("gas_usage", 0),
            data.get("heating_oil", 0)
        )
        
        # Transportation
        transport_emissions = CarbonCalculator.calculate_transportation_emissions(
            data.get("vehicle_miles", 0),
            data.get("public_transport_km", 0),
            data.get("flights_km", 0)
        )
        
        # Waste
        waste_emissions = CarbonCalculator.calculate_waste_emissions(
            data.get("waste_produced", 0),
            data.get("recycling_rate", 0)
        )
        
        # Food
        food_emissions = CarbonCalculator.calculate_food_emissions(
            data.get("meat_consumption", 0),
            data.get("vegetarian_meals", 0)
        )
        
        # Water
        water_emissions = CarbonCalculator.calculate_water_emissions(
            data.get("water_usage", 0)
        )
        
        # Corporate/Institutional (if applicable)
        corporate_emissions = 0
        user_type = data.get("user_type", "individual")
        if user_type in ["corporation", "institution"]:
            corporate_emissions = CarbonCalculator.calculate_corporate_emissions(
                data.get("employee_count", 1),
                data.get("office_space_sqm", 0),
                data.get("manufacturing_output", 0),
                data.get("supply_chain_distance", 0)
            )
        
        # Total
        total_emissions = (
            energy_emissions +
            transport_emissions +
            waste_emissions +
            food_emissions +
            water_emissions +
            corporate_emissions
        )
        
        # Per person calculation if applicable
        employee_count = data.get("employee_count", 1)
        per_person_emissions = total_emissions / employee_count if employee_count > 0 else total_emissions
        
        breakdown = {
            "energy": round(energy_emissions, 2),
            "transportation": round(transport_emissions, 2),
            "waste": round(waste_emissions, 2),
            "food": round(food_emissions, 2),
            "water": round(water_emissions, 2),
            "corporate": round(corporate_emissions, 2),
            "total": round(total_emissions, 2),
            "per_person": round(per_person_emissions, 2)
        }
        
        return breakdown

