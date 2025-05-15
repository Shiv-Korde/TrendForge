import pandas as pd
import numpy as np
from io import BytesIO
import asammdf
import nptdms
import os

def load_testbench_data(file):
    file_name = file.name.lower()
    
    if file_name.endswith(".txt"):
        try:
            # Read all lines
            content = file.read().decode("utf-8").splitlines()

            # Extract metadata (all lines before the 'Timestamp' header)
            header_line_index = next(i for i, line in enumerate(content) if line.strip().startswith("Timestamp"))
            metadata_lines = content[:header_line_index]
            metadata = "\n".join(metadata_lines)

            # Parse data section
            header = content[header_line_index].strip().split("\t")
            data = [
                line.strip().split("\t")
                for line in content[header_line_index + 1:]
                if len(line.strip().split("\t")) == len(header)
            ]

            df = pd.DataFrame(data, columns=header)
            df["timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
            df.drop(columns=["Timestamp"], inplace=True)
            for col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

            return metadata, df.dropna(subset=["timestamp"])
        except Exception as e:
            print("Error loading TXT:", e)
            return None, None
        
    elif file_name.endswith(".dat") or file_name.endswith(".mf4"):
        try:
            mdf = asammdf.MDF(BytesIO(file.read()))
            return mdf.to_dataframe()
        except Exception:
            return None

    elif file_name.endswith(".tdms"):
        try:
            tdms_file = nptdms.TdmsFile(BytesIO(file.read()))
            df = tdms_file.as_dataframe()
            return df
        except Exception:
            return None

    elif file_name.endswith(".lvm"):
        try:
            return pd.read_csv(file, sep='\t', comment='#')
        except Exception:
            return None

    return None

def detect_anomalies(df):
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if not numeric_cols:
        return "No numeric data available for anomaly detection."

    anomalies = {}
    for col in numeric_cols:
        mean = df[col].mean()
        std = df[col].std()
        outliers = df[(df[col] > mean + 3 * std) | (df[col] < mean - 3 * std)]
        if not outliers.empty:
            anomalies[col] = outliers.shape[0]

    return anomalies if anomalies else "No anomalies detected."
