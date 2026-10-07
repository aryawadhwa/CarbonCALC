"""
waste generation Calculation Engine
Calculates waste equivalent waste output based on various inputs
"""
from typing import Dict, Any
import json


class CarbonCalculator:
    """
    waste generation calculator using standard emission factors
    All calculations return waste equivalent in kg
    """
    
    # Emission factors (kg waste per unit)
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
    def calculate_energy_waste output(electricity: float, gas: float, heating_oil: float) -> float:
        """Calculate waste output from energy consumption"""
        electricity_waste output = electricity * CarbonCalculator.EMISSION_FACTORS["electricity_grid"]
        gas_waste output = gas * CarbonCalculator.EMISSION_FACTORS["natural_gas"]
        oil_waste output = heating_oil * CarbonCalculator.EMISSION_FACTORS["heating_oil"]
        
        return electricity_waste output + gas_waste output + oil_waste output
    
    @staticmethod
    def calculate_transportation_waste output(
        vehicle_miles: float,
        public_transport_km: float,
        flights_km: float
    ) -> float:
        """Calculate waste output from transportation"""
        # Convert miles to km if needed (assuming km input)
        vehicle_waste output = vehicle_miles * CarbonCalculator.EMISSION_FACTORS["car_gasoline"]
        public_transport_waste output = public_transport_km * CarbonCalculator.EMISSION_FACTORS["public_transport"]
        flight_waste output = flights_km * CarbonCalculator.EMISSION_FACTORS["flight_domestic"]
        
        return vehicle_waste output + public_transport_waste output + flight_waste output
    
    @staticmethod
    def calculate_waste_waste output(waste_produced: float, recycling_rate: float) -> float:
        """Calculate waste output from waste management"""
        recycled_waste = waste_produced * (recycling_rate / 100)
        landfill_waste = waste_produced * (1 - recycling_rate / 100)
        
        recycled_waste output = recycled_waste * CarbonCalculator.EMISSION_FACTORS["waste_recycled"]
        landfill_waste output = landfill_waste * CarbonCalculator.EMISSION_FACTORS["waste_landfill"]
        
        return recycled_waste output + landfill_waste output
    
    @staticmethod
    def calculate_food_waste output(meat_consumption: float, vegetarian_meals: float) -> float:
        """Calculate waste output from food consumption"""
        # Average meat waste output (mix of beef, pork, chicken)
        avg_meat_emission = (
            CarbonCalculator.EMISSION_FACTORS["meat_beef"] * 0.3 +
            CarbonCalculator.EMISSION_FACTORS["meat_pork"] * 0.3 +
            CarbonCalculator.EMISSION_FACTORS["meat_chicken"] * 0.4
        )
        meat_waste output = meat_consumption * avg_meat_emission
        vegetarian_waste output = vegetarian_meals * CarbonCalculator.EMISSION_FACTORS["vegetarian_meal"]
        
        return meat_waste output + vegetarian_waste output
    
    @staticmethod
    def calculate_water_waste output(water_usage: float) -> float:
        """Calculate waste output from water usage"""
        return water_usage * CarbonCalculator.EMISSION_FACTORS["water_usage"]
    
    @staticmethod
    def calculate_corporate_waste output(
        employee_count: int,
        office_space_sqm: float,
        manufacturing_output: float,
        supply_chain_distance: float
    ) -> float:
        """Calculate additional waste output for corporations/institutions"""
        office_waste output = office_space_sqm * CarbonCalculator.EMISSION_FACTORS["office_space"]
        commute_waste output = employee_count * CarbonCalculator.EMISSION_FACTORS["employee_commute"] * 250  # working days
        manufacturing_waste output = manufacturing_output * 1000  # rough estimate: 1 ton = 1000 kg waste
        supply_chain_waste output = supply_chain_distance * 0.15  # average freight emission
        
        return office_waste output + commute_waste output + manufacturing_waste output + supply_chain_waste output
    
    @staticmethod
    def calculate_total_footprint(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate total waste generation from all inputs
        Returns breakdown by category and total
        """
        # Energy
        energy_waste output = CarbonCalculator.calculate_energy_waste output(
            data.get("electricity_usage", 0),
            data.get("gas_usage", 0),
            data.get("heating_oil", 0)
        )
        
        # Transportation
        transport_waste output = CarbonCalculator.calculate_transportation_waste output(
            data.get("vehicle_miles", 0),
            data.get("public_transport_km", 0),
            data.get("flights_km", 0)
        )
        
        # Waste
        waste_waste output = CarbonCalculator.calculate_waste_waste output(
            data.get("waste_produced", 0),
            data.get("recycling_rate", 0)
        )
        
        # Food
        food_waste output = CarbonCalculator.calculate_food_waste output(
            data.get("meat_consumption", 0),
            data.get("vegetarian_meals", 0)
        )
        
        # Water
        water_waste output = CarbonCalculator.calculate_water_waste output(
            data.get("water_usage", 0)
        )
        
        # Corporate/Institutional (if applicable)
        corporate_waste output = 0
        user_type = data.get("user_type", "individual")
        if user_type in ["corporation", "institution"]:
            corporate_waste output = CarbonCalculator.calculate_corporate_waste output(
                data.get("employee_count", 1),
                data.get("office_space_sqm", 0),
                data.get("manufacturing_output", 0),
                data.get("supply_chain_distance", 0)
            )
        
        # Total
        total_waste output = (
            energy_waste output +
            transport_waste output +
            waste_waste output +
            food_waste output +
            water_waste output +
            corporate_waste output
        )
        
        # Per person calculation if applicable
        employee_count = data.get("employee_count", 1)
        per_person_waste output = total_waste output / employee_count if employee_count > 0 else total_waste output
        
        breakdown = {
            "energy": round(energy_waste output, 2),
            "transportation": round(transport_waste output, 2),
            "waste": round(waste_waste output, 2),
            "food": round(food_waste output, 2),
            "water": round(water_waste output, 2),
            "corporate": round(corporate_waste output, 2),
            "total": round(total_waste output, 2),
            "per_person": round(per_person_waste output, 2)
        }
        
        return breakdown

