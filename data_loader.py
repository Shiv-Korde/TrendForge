import pandas as pd
from io import BytesIO
from asammdf import MDF
from nptdms import TdmsFile

def load_testbench_data(file):
    file_name = file.name.lower()

    if file_name.endswith(".txt") or file_name.endswith(".lvm"):
        try:
            lines = file.read().decode("utf-8").splitlines()
            meta_lines = []
            data_lines = []
            header_found = False

            for line in lines:
                if not header_found and "Timestamp" in line:
                    header = line.strip()
                    header_found = True
                    continue
                if not header_found:
                    meta_lines.append(line.strip())
                else:
                    data_lines.append(line.strip())

            if not header_found or not data_lines:
                return None, None  # Failed to detect valid data

            # Parse measurement data
            header_cols = header.split("\t")
            clean_rows = [row.split("\t") for row in data_lines if len(row.split("\t")) == len(header_cols)]
            df = pd.DataFrame(clean_rows, columns=header_cols)
            df["timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
            df.drop(columns=["Timestamp"], inplace=True)
            for col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

            meta_text = "\n".join(meta_lines)
            return meta_text, df.dropna(subset=["timestamp"])

        except Exception as e:
            print("Text/LVM parsing error:", e)
            return None, None

    elif file_name.endswith(".mf4") or file_name.endswith(".dat"):
        try:
            mdf = MDF(BytesIO(file.read()))
            meta_text = f"File Version: {mdf.version}, Number of Channels: {len(mdf.channels_db)}"
            return meta_text, mdf.to_dataframe()
        except Exception as e:
            print("MDF parsing error:", e)
            return None, None

    elif file_name.endswith(".tdms"):
        try:
            tdms_file = TdmsFile(BytesIO(file.read()))
            meta_text = f"Groups: {len(tdms_file.groups())}, Channels: {sum(len(g.channels()) for g in tdms_file.groups())}"
            return meta_text, tdms_file.as_dataframe()
        except Exception as e:
            print("TDMS parsing error:", e)
            return None, None

    return None, None
