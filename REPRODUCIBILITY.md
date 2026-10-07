# MLOps Reproducibility Guide (Phase 1)

This project strictly follows MLOps Phase 1 guidelines (Development & Reproducibility) to ensure that model training, data exploration, and evaluation can be systematically reproduced. 

Because the project relies on restricted real-world data, the raw dataset is intentionally excluded from the Git repository. 

## 1. Setup

Install the required MLOps dependencies (DVC, MLflow, Jupyter, etc.):
```bash
pip install -r requirements-dev.txt
```

## 2. Dataset Acquisition & DVC Tracking

Once you have acquired the approved dataset, place it in the `data/raw/` directory:
```bash
mv path/to/your/real_dataset.csv data/raw/dataset.csv
```

To securely track this dataset using Data Version Control (DVC) without committing the raw data to GitHub:
```bash
dvc add data/raw/dataset.csv
git add data/raw/dataset.csv.dvc
git commit -m "data: Track raw dataset with DVC"
```

## 3. Data Exploration (EDA)

A Jupyter notebook template is provided to ensure standardized data exploration:
```bash
jupyter notebook notebooks/01_EDA.ipynb
```
The notebook is pre-configured to load `data/raw/dataset.csv` and contains structural placeholders for distribution and correlation analysis.

## 4. Model Training & MLflow Experiment Tracking

To ensure reproducibility, model training is decoupled from the backend application and managed via a dedicated script. The script trains baseline and advanced ensemble models, automatically logging all parameters and evaluation metrics (R², MAE, RMSE) to MLflow.

Run the training pipeline:
```bash
python scripts/train.py
```

To review the experiments, launch the MLflow UI:
```bash
mlflow ui
```
Navigate to `http://localhost:5000` to compare model performance metrics and access serialized model artifacts.
