import pandas as pd
import mlflow
import os
import sys

# Append backend to path to import the predictor model
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))
from ml_models.predictor import WasteGenerationPredictor

def main():
    # Set up MLflow tracking
    mlflow.set_experiment("Waste_Management_Model_Training")
    
    # The real dataset is expected to be placed here by the user/researcher
    dataset_path = "data/raw/dataset.csv"
    
    if not os.path.exists(dataset_path):
        print(f"Error: Dataset not found at '{dataset_path}'.")
        print("Please place your approved real dataset in 'data/raw/dataset.csv' before running the training script.")
        return

    # Load dataset
    print(f"Loading dataset from {dataset_path}...")
    df = pd.read_csv(dataset_path)
    
    # Convert to the list of dictionaries expected by the backend predictor
    historical_data = df.to_dict('records')
    
    # Define models to train
    model_types = ['lightweight', 'random_forest', 'gradient_boosting', 'ensemble']
    
    # Train and evaluate each model with MLflow tracking
    for model_type in model_types:
        with mlflow.start_run(run_name=f"{model_type}_training"):
            print(f"\nTraining {model_type} model...")
            
            # Log parameters
            mlflow.log_param("model_type", model_type)
            mlflow.log_param("dataset_size", len(historical_data))
            
            predictor = WasteGenerationPredictor(model_type=model_type)
            metrics = predictor.train(historical_data)
            
            if "error" in metrics:
                print(f"Failed to train {model_type}: {metrics['error']}")
                continue
                
            # Log evaluation metrics
            mlflow.log_metric("mse", metrics["mse"])
            mlflow.log_metric("mae", metrics["mae"])
            mlflow.log_metric("rmse", metrics["rmse"])
            mlflow.log_metric("r2_score", metrics["r2_score"])
            
            # Log feature importances if it's a tree-based model
            if hasattr(predictor.model, 'feature_importances_'):
                importances = predictor.model.feature_importances_
                for i, imp in enumerate(importances):
                    mlflow.log_metric(f"feature_{i}_importance", imp)
            
            print(f"Results for {model_type}: R2 = {metrics['r2_score']:.4f}, MAE = {metrics['mae']:.4f}")
            
            # Save model to models directory
            os.makedirs("models", exist_ok=True)
            model_path = f"models/{model_type}_model.pkl"
            predictor.save_model(model_path)
            
            # Log model as an artifact in MLflow
            mlflow.log_artifact(model_path)
            
    print("\nTraining complete. Run 'mlflow ui' to view the experiment results.")

if __name__ == "__main__":
    main()
