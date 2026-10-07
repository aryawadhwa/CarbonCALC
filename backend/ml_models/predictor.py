"""
Machine Learning Models for Carbon Footprint Prediction and Forecasting
Research-grade predictive analytics using time series and regression models
"""
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib
import os
from typing import List, Dict, Tuple, Optional
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')


class CarbonFootprintPredictor:
    """
    Advanced ML-based carbon footprint prediction system
    Uses ensemble methods for accurate forecasting
    """
    
    def __init__(self, model_type: str = "ensemble"):
        """
        Initialize predictor
        Args:
            model_type: 'ensemble', 'random_forest', 'gradient_boosting', 'linear', or 'lightweight'
            Note: All models run on CPU - no GPU required. Optimized for low-resource environments.
            'lightweight' uses simple linear regression for minimal compute requirements.
        """
        self.model_type = model_type
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = None
        self.is_trained = False
        
    def prepare_features(self, historical_data: List[Dict]) -> Tuple[np.ndarray, np.ndarray]:
        """
        Prepare features from historical carbon footprint data
        Extracts temporal patterns, trends, and seasonal features
        """
        if not historical_data:
            return np.array([]), np.array([])
        
        df = pd.DataFrame(historical_data)
        
        # Sort by date
        if 'entry_date' in df.columns:
            df['entry_date'] = pd.to_datetime(df['entry_date'])
            df = df.sort_values('entry_date')
        
        # Extract features
        features = []
        targets = []
        
        # Create time-based features
        df['days_since_start'] = (df['entry_date'] - df['entry_date'].min()).dt.days if 'entry_date' in df.columns else range(len(df))
        df['month'] = df['entry_date'].dt.month if 'entry_date' in df.columns else [datetime.now().month] * len(df)
        df['quarter'] = df['entry_date'].dt.quarter if 'entry_date' in df.columns else [1] * len(df)
        
        # Create rolling statistics
        window_size = min(3, len(df))
        if window_size > 0:
            df['rolling_mean'] = df['total_carbon_footprint'].rolling(window=window_size, min_periods=1).mean()
            df['rolling_std'] = df['total_carbon_footprint'].rolling(window=window_size, min_periods=1).std().fillna(0)
            df['trend'] = df['total_carbon_footprint'].diff().fillna(0)
        
        for i in range(len(df)):
            row_features = []
            
            # Temporal features
            row_features.append(df.iloc[i]['days_since_start'])
            row_features.append(df.iloc[i]['month'])
            row_features.append(df.iloc[i]['quarter'])
            
            # Statistical features
            if 'rolling_mean' in df.columns:
                row_features.append(df.iloc[i]['rolling_mean'])
            else:
                row_features.append(df.iloc[i]['total_carbon_footprint'])
            
            if 'rolling_std' in df.columns:
                row_features.append(df.iloc[i]['rolling_std'])
            else:
                row_features.append(0)
            
            if 'trend' in df.columns:
                row_features.append(df.iloc[i]['trend'])
            else:
                row_features.append(0)
            
            # Category breakdown features (if available)
            if 'category_breakdown' in df.columns and df.iloc[i]['category_breakdown']:
                breakdown = df.iloc[i]['category_breakdown']
                if isinstance(breakdown, str):
                    import json
                    breakdown = json.loads(breakdown)
                
                categories = ['energy', 'transportation', 'waste', 'food', 'water', 'corporate']
                for cat in categories:
                    row_features.append(breakdown.get(cat, 0))
            else:
                # Default zeros for categories
                row_features.extend([0] * 6)
            
            features.append(row_features)
            targets.append(df.iloc[i]['total_carbon_footprint'])
        
        self.feature_names = [
            'days_since_start', 'month', 'quarter', 'rolling_mean', 'rolling_std', 'trend',
            'energy', 'transportation', 'waste', 'food', 'water', 'corporate'
        ]
        
        return np.array(features), np.array(targets)
    
    def train(self, historical_data: List[Dict]) -> Dict[str, float]:
        """
        Train the prediction model on historical data
        Returns training metrics
        """
        if not historical_data or len(historical_data) < 2:
            return {"error": "Insufficient data for training"}
        
        X, y = self.prepare_features(historical_data)
        
        if len(X) < 2:
            return {"error": "Insufficient samples for training"}
        
        # Split data
        if len(X) > 3:
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        else:
            X_train, X_test, y_train, y_test = X, X, y, y
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test) if len(X_test) > 0 else X_train_scaled
        
        # Train model based on type (optimized for CPU, no GPU needed)
        # Lightweight configuration for low-resource environments
        n_estimators = 50  # Reduced from 100 for faster training
        max_depth_rf = 8   # Reduced from 10
        max_depth_gb = 4   # Reduced from 5
        
        if self.model_type == "ensemble":
            rf = RandomForestRegressor(
                n_estimators=n_estimators, 
                max_depth=max_depth_rf, 
                random_state=42,
                n_jobs=-1  # Use all CPU cores
            )
            gb = GradientBoostingRegressor(
                n_estimators=n_estimators, 
                max_depth=max_depth_gb, 
                random_state=42,
                learning_rate=0.1
            )
            rf.fit(X_train_scaled, y_train)
            gb.fit(X_train_scaled, y_train)
            # Use ensemble prediction
            self.model = (rf, gb)
        elif self.model_type == "random_forest":
            self.model = RandomForestRegressor(
                n_estimators=n_estimators, 
                max_depth=max_depth_rf, 
                random_state=42,
                n_jobs=-1
            )
            self.model.fit(X_train_scaled, y_train)
        elif self.model_type == "gradient_boosting":
            self.model = GradientBoostingRegressor(
                n_estimators=n_estimators, 
                max_depth=max_depth_gb, 
                random_state=42
            )
            self.model.fit(X_train_scaled, y_train)
        elif self.model_type == "lightweight":
            # Ultra-lightweight linear model for minimal compute
            self.model = LinearRegression()
            self.model.fit(X_train_scaled, y_train)
        else:  # linear
            self.model = LinearRegression()
            self.model.fit(X_train_scaled, y_train)
        
        # Evaluate
        if len(X_test) > 0:
            if isinstance(self.model, tuple):
                y_pred_rf = self.model[0].predict(X_test_scaled)
                y_pred_gb = self.model[1].predict(X_test_scaled)
                y_pred = (y_pred_rf + y_pred_gb) / 2
            else:
                y_pred = self.model.predict(X_test_scaled)
            
            mse = mean_squared_error(y_test, y_pred)
            mae = mean_absolute_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            rmse = np.sqrt(mse)
        else:
            mse = mae = r2 = rmse = 0.0
        
        self.is_trained = True
        
        return {
            "mse": float(mse),
            "mae": float(mae),
            "rmse": float(rmse),
            "r2_score": float(r2),
            "training_samples": len(X_train),
            "test_samples": len(X_test)
        }
    
    def predict(self, historical_data: List[Dict], forecast_periods: int = 12) -> Dict:
        """
        Predict future carbon footprint
        Args:
            historical_data: List of historical entries
            forecast_periods: Number of future periods to predict
        Returns:
            Dictionary with predictions, confidence intervals, and metrics
        """
        if not self.is_trained:
            # Train first if not trained
            self.train(historical_data)
        
        if not historical_data:
            return {"error": "No historical data provided"}
        
        # Prepare last known features
        X, y = self.prepare_features(historical_data)
        if len(X) == 0:
            return {"error": "Could not prepare features"}
        
        last_features = X[-1].reshape(1, -1)
        last_footprint = y[-1] if len(y) > 0 else 0
        
        # Generate predictions for future periods
        predictions = []
        confidence_intervals = []
        
        current_features = last_features.copy()
        
        for period in range(1, forecast_periods + 1):
            # Scale features
            current_scaled = self.scaler.transform(current_features)
            
            # Predict
            if isinstance(self.model, tuple):
                pred_rf = self.model[0].predict(current_scaled)[0]
                pred_gb = self.model[1].predict(current_scaled)[0]
                prediction = (pred_rf + pred_gb) / 2
                # Estimate confidence from model variance
                std_est = abs(pred_rf - pred_gb) / 2
            else:
                prediction = self.model.predict(current_scaled)[0]
                std_est = abs(prediction - last_footprint) * 0.1  # Rough estimate
            
            predictions.append(float(prediction))
            confidence_intervals.append({
                "lower": float(max(0, prediction - 1.96 * std_est)),
                "upper": float(prediction + 1.96 * std_est)
            })
            
            # Update features for next prediction
            # Increment temporal features
            current_features[0][0] += 30  # Add 30 days
            current_features[0][1] = ((current_features[0][1] + 1) % 12) + 1  # Increment month
            current_features[0][2] = ((current_features[0][2] - 1) % 4) + 1  # Update quarter
            
            # Update rolling mean (simplified)
            current_features[0][3] = (current_features[0][3] + prediction) / 2
        
        # Calculate trend analysis
        historical_values = [entry.get('total_carbon_footprint', 0) for entry in historical_data]
        if len(historical_values) > 1:
            trend = "increasing" if historical_values[-1] > historical_values[0] else "decreasing"
            avg_change = (historical_values[-1] - historical_values[0]) / len(historical_values)
        else:
            trend = "stable"
            avg_change = 0
        
        return {
            "predictions": predictions,
            "confidence_intervals": confidence_intervals,
            "forecast_periods": forecast_periods,
            "current_footprint": float(last_footprint),
            "projected_annual": float(predictions[-1] * 12) if predictions else 0,
            "trend_analysis": {
                "trend": trend,
                "average_change_per_period": float(avg_change),
                "projected_reduction_potential": float(max(0, last_footprint - predictions[-1])) if predictions else 0
            }
        }
    
    def save_model(self, filepath: str):
        """Save trained model to disk"""
        os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else '.', exist_ok=True)
        model_data = {
            'model_type': self.model_type,
            'model': self.model,
            'scaler': self.scaler,
            'feature_names': self.feature_names,
            'is_trained': self.is_trained
        }
        joblib.dump(model_data, filepath)
    
    @classmethod
    def load_model(cls, filepath: str):
        """Load trained model from disk"""
        model_data = joblib.load(filepath)
        predictor = cls(model_type=model_data['model_type'])
        predictor.model = model_data['model']
        predictor.scaler = model_data['scaler']
        predictor.feature_names = model_data['feature_names']
        predictor.is_trained = model_data['is_trained']
        return predictor

