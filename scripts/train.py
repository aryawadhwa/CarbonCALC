import pandas as pd
import numpy as np
import mlflow
import os
import sys

# Add root directory to Python path so we can import from ml_models
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ml_models.predictor import CarbonFootprintPredictor

def train_and_evaluate():
    # Set MLflow experiment
    mlflow.set_experiment("CarbonCALC_Baseline_Models")
    
    data_path = "data/raw/synthetic_carbon_data.csv"
    if not os.path.exists(data_path):
        print(f"Data file not found at {data_path}. Please run generate_data.py first.")
        return
        
    df = pd.read_csv(data_path)
    # Convert to list of dicts as expected by the predictor
    historical_data = df.to_dict('records')
    
    models = ['lightweight', 'random_forest', 'gradient_boosting', 'ensemble']
    
    for model_type in models:
        with mlflow.start_run(run_name=f"{model_type}_baseline"):
            print(f"Training {model_type} model...")
            
            # Log model parameters
            mlflow.log_param("model_type", model_type)
            mlflow.log_param("dataset_size", len(historical_data))
            
            predictor = CarbonFootprintPredictor(model_type=model_type)
            metrics = predictor.train(historical_data)
            
            if "error" in metrics:
                print(f"Error training {model_type}: {metrics['error']}")
                continue
                
            # Log metrics
            mlflow.log_metric("mse", metrics["mse"])
            mlflow.log_metric("mae", metrics["mae"])
            mlflow.log_metric("rmse", metrics["rmse"])
            mlflow.log_metric("r2_score", metrics["r2_score"])
            
            print(f"{model_type} - R2: {metrics['r2_score']:.4f}, MAE: {metrics['mae']:.4f}")
            
            # Save and log model artifact
            model_path = f"models/{model_type}_model.pkl"
            predictor.save_model(model_path)
            mlflow.log_artifact(model_path)

if __name__ == "__main__":
    os.makedirs("models", exist_ok=True)
    train_and_evaluate()
