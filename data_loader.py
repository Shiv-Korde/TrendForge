import pandas as pd
from io import BytesIO
from asammdf import MDF
from nptdms import TdmsFile

def load_testbench_data(file):
    file_name = file.name.lower()
    try:
        if file_name.endswith(".txt"):
            return pd.read_csv(file, sep=None, engine='python', encoding='utf-8', on_bad_lines='skip')
        elif file_name.endswith(".lvm"):
            return pd.read_csv(file, sep='\\t', engine='python', comment='#')
        elif file_name.endswith(".mf4") or file_name.endswith(".dat"):
            mdf = MDF(BytesIO(file.read()))
            return mdf.to_dataframe()
        elif file_name.endswith(".tdms"):
            tdms_file = TdmsFile(BytesIO(file.read()))
            return tdms_file.as_dataframe()
    except Exception as e:
        print(f"Error loading file: {e}")
    return None
