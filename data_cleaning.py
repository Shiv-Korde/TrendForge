import pandas as pd

def clean_data(df: pd.DataFrame, method: str) -> pd.DataFrame:
    if method == "Drop Rows":
        return df.dropna()
    elif method == "Fill with 0":
        return df.fillna(0)
    elif method == "Forward Fill":
        return df.ffill()
    elif method == "Backward Fill":
        return df.bfill()
    else:
        return df  # default (no change)
import pandas as pd

def clean_data(df: pd.DataFrame, method: str) -> pd.DataFrame:
    if method == "Drop Rows":
        return df.dropna()
    elif method == "Fill with 0":
        return df.fillna(0)
    elif method == "Forward Fill":
        return df.ffill()
    elif method == "Backward Fill":
        return df.bfill()
    else:
        return df  # default (no change)
