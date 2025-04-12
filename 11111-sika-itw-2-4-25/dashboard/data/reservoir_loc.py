import re
import time

import pandas as pd
import requests


def clean_location_name(full_name):
    # Extract only the reservoir name (before any comma)
    match = re.match(r"(Reservoir [^,]+)", full_name)
    return match.group(1) if match else full_name


def geocode_location(location):
    query = f"{location}, Zürich, Switzerland"
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": query,
        "format": "json",
        "limit": 1
    }
    response = requests.get(url, params=params, headers={
                            "User-Agent": "streamlit-reservoir-map"})
    if response.status_code == 200 and response.json():
        result = response.json()[0]
        return float(result["lat"]), float(result["lon"])
    else:
        return None, None


# Load dataset
df = pd.read_csv("data/reservoir_data.csv")
df = df.dropna(subset=["Standort"])
df["CleanedName"] = df["Standort"].apply(clean_location_name)

# Geocode unique cleaned names
unique_cleaned_names = df["CleanedName"].unique()
geocoded_data = {}

for name in unique_cleaned_names:
    lat, lon = geocode_location(name)
    print(f"{name} → {lat}, {lon}")
    geocoded_data[name] = {"lat": lat, "lon": lon}
    time.sleep(1)  # respect API rate limits

# Map geocoded coordinates back to original DataFrame
df["lat"] = df["CleanedName"].map(
    lambda x: geocoded_data.get(x, {}).get("lat"))
df["lon"] = df["CleanedName"].map(
    lambda x: geocoded_data.get(x, {}).get("lon"))

# Save enriched dataset
output_path = "data/reservoir_data_geocoded.csv"
df.to_csv(output_path, index=False)
print(f"Saved with coordinates → {output_path}")
