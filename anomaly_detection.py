import pandas as pd
import numpy as np

def detect_anomalies(df: pd.DataFrame) -> dict:
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if not numeric_cols:
        return {"message": "No numeric columns for anomaly detection."}

    anomalies = {}
    for col in numeric_cols:
        mean = df[col].mean()
        std = df[col].std()
        outliers = df[(df[col] > mean + 3 * std) | (df[col] < mean - 3 * std)]
        if not outliers.empty:
            anomalies[col] = outliers.shape[0]

    return anomalies if anomalies else {"message": "No anomalies detected."}
