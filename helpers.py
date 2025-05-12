import pandas as pd
import numpy as np

def load_testbench_data(file):
    content = file.read().decode("utf-8").splitlines()
    data_start_idx = None
    for i, line in enumerate(content):
        if line.strip().startswith("Timestamp"):
            data_start_idx = i
            break
    if data_start_idx is None:
        raise ValueError("No valid header line starting with 'Timestamp' found.")
    header = content[data_start_idx].strip().split("\t")
    data_lines = content[data_start_idx + 1:]
    cleaned_data = []
    for line in data_lines:
        cols = line.strip().split("\t")
        if len(cols) == len(header):
            cleaned_data.append(cols)
    df = pd.DataFrame(cleaned_data, columns=header)
    df["timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
    df.drop(columns=["Timestamp"], inplace=True)
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df.dropna(subset=["timestamp"])

def detect_anomalies(df, col, threshold=3.0):
    z_scores = (df[col] - df[col].mean()) / df[col].std()
    return df[np.abs(z_scores) > threshold]