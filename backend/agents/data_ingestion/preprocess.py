import pandas as pd

# Clean data (e.g., remove missing values)
def clean_data(data):
    return data.dropna()

# Normalize numeric data
def normalize_data(data):
    return (data - data.min()) / (data.max() - data.min())

# Preprocess CSV
def preprocess_csv(file_path):
    data = ingest_csv(file_path)
    if data is not None:
        data = clean_data(data)
        data = normalize_data(data)
        return data
    return None