import pandas as pd
import os

# Set the data directory relative to this script
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
INPUT_CSV = os.path.join(DATA_DIR, "climbing_gyms.csv")
OUTPUT_CSV = os.path.join(DATA_DIR, "processed_climbing_gyms.csv")

# Function to process the Description column
def process_description(description):
    if pd.isna(description):
        return None, None, None

    lines = description.strip().split('\n')

    opening_hours = None
    contact_number = None
    features = []

    for line in lines:
        line = line.strip()
        if line.lower().startswith("opening hours"):
            opening_hours = line
        elif line.lower().startswith("contact"):
            contact_number = line
        else:
            features.append(line)

    features_str = "; ".join(features)
    return opening_hours, contact_number, features_str

# Read the CSV
df = pd.read_csv(INPUT_CSV)

# Apply the processing function
df[['Opening Hours', 'Contact Number', 'Features']] = df['Description'].apply(
    lambda x: pd.Series(process_description(x))
)

# Save to processed CSV
df.to_csv(OUTPUT_CSV, index=False)

print(f"CSV file has been processed and saved as '{OUTPUT_CSV}'")
