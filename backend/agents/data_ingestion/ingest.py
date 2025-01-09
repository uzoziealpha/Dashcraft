import pandas as pd
import json
import os
from werkzeug.utils import secure_filename

# Ingest CSV data
def ingest_csv(file_path):
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return None

# Ingest JSON data
def ingest_json(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"Error reading JSON: {e}")
        return None