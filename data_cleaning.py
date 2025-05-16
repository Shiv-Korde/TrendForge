import pandas as pd

def clean_data(df: pd.DataFrame, method: str, column: str = None) -> pd.DataFrame:
    if column:
        if method == "Fill with 0":
            df[column] = df[column].fillna(0)
        elif method == "Forward Fill":
            df[column] = df[column].ffill()
        elif method == "Backward Fill":
            df[column] = df[column].bfill()
        return df

    if method == "Drop Rows":
        return df.dropna()
    elif method == "Fill with 0":
        return df.fillna(0)
    elif method == "Forward Fill":
        return df.ffill()
    elif method == "Backward Fill":
        return df.bfill()
    return df


def auto_clean(df: pd.DataFrame) -> pd.DataFrame:
    for col in df.columns:
        if df[col].dtype in ["float64", "int64"]:
            df[col] = df[col].ffill().fillna(0)
        else:
            df[col] = df[col].ffill()
    return df.dropna()
