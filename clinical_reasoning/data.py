import pandas as pd
from typing import List

def load_mimic_notes(csv_path: str) -> List[str]:
    try:
        df = pd.read_csv(csv_path)
        clinical_notes = df['TEXT'].dropna().tolist()
        print(f"Loaded {len(clinical_notes)} clinical notes from CSV")
        return clinical_notes
    except FileNotFoundError:
        print(f"Error: File {csv_path} not found")
        return []
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return []
