import numpy as np
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_percentage_error
import math

def calculate_metrics(y_true, y_pred):
    """Menghitung RMSE, R2, dan MAPE"""
    rmse = math.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)
    mape = mean_absolute_percentage_error(y_true, y_pred) * 100
    
    return {
        'RMSE': rmse,
        'R2': r2,
        'MAPE': mape
    }

def print_metrics(metrics, model_name):
    print(f"\n[{model_name}] Hasil Evaluasi:")
    print(f"  R2 Score : {metrics['R2']:.4f}")
    print(f"  RMSE     : {metrics['RMSE']:.2f} Kg")
    print(f"  MAPE     : {metrics['MAPE']:.2f}% (Tingkat Error)")