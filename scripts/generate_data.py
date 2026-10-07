import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import json

def generate_synthetic_data(n_users=100, entries_per_user=12):
    """Generate synthetic carbon footprint data mimicking user entries."""
    np.random.seed(42)
    data = []
    
    start_date = datetime.now() - timedelta(days=365)
    
    for user_id in range(1, n_users + 1):
        # User profile
        user_type = np.random.choice(['individual', 'institution', 'corporation'], p=[0.7, 0.2, 0.1])
        base_footprint = {'individual': 500, 'institution': 5000, 'corporation': 20000}[user_type]
        
        # Add entries over time
        for entry_idx in range(entries_per_user):
            entry_date = start_date + timedelta(days=30 * entry_idx + np.random.randint(-5, 5))
            
            # Simulate a decreasing trend for most users as they use the app
            trend_factor = 1.0 - (entry_idx * 0.02) 
            
            # Add some random noise and seasonality
            seasonality = 1.0 + 0.1 * np.sin(entry_date.month * np.pi / 6)
            noise = np.random.normal(1.0, 0.05)
            
            total_footprint = base_footprint * trend_factor * seasonality * noise
            
            # Break down into categories
            energy = total_footprint * np.random.uniform(0.3, 0.5)
            transportation = total_footprint * np.random.uniform(0.2, 0.4)
            waste = total_footprint * np.random.uniform(0.05, 0.15)
            food = total_footprint * np.random.uniform(0.1, 0.2)
            water = total_footprint * np.random.uniform(0.02, 0.08)
            corporate = 0
            
            if user_type != 'individual':
                corporate = total_footprint * np.random.uniform(0.2, 0.5)
                # re-normalize
                total_cat = energy + transportation + waste + food + water + corporate
                ratio = total_footprint / total_cat
                energy *= ratio; transportation *= ratio; waste *= ratio; food *= ratio; water *= ratio; corporate *= ratio
                
            breakdown = {
                "energy": energy,
                "transportation": transportation,
                "waste": waste,
                "food": food,
                "water": water,
                "corporate": corporate
            }
            
            data.append({
                "user_id": user_id,
                "user_type": user_type,
                "entry_date": entry_date.strftime("%Y-%m-%d"),
                "total_carbon_footprint": total_footprint,
                "category_breakdown": json.dumps(breakdown)
            })
            
    df = pd.DataFrame(data)
    os.makedirs("data/raw", exist_ok=True)
    df.to_csv("data/raw/synthetic_carbon_data.csv", index=False)
    print(f"Generated {len(df)} records in data/raw/synthetic_carbon_data.csv")

if __name__ == "__main__":
    generate_synthetic_data()
