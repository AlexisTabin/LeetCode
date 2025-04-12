import re
import time

import pandas as pd
import requests

# Step 1: Load and clean
df = pd.read_csv("data/water_treatment_data.csv")
df = df.dropna(subset=["Standort"])

# Step 2: Simplify Standort (e.g., "Seewasserwerk Moos, Reinwasser" → "Seewasserwerk Moos")


def clean_treatment_location(name):
    match = re.match(r"(Seewasserwerk [^,]+)", name)
    return match.group(1) if match else name


df["CleanedName"] = df["Standort"].apply(clean_treatment_location)

# Step 3: Geocode unique names
unique_places = df["CleanedName"].unique()
geocoded = {}


def geocode_place(place):
    query = f"{place}, Zürich, Switzerland"
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": query, "format": "json", "limit": 1}
    headers = {"User-Agent": "streamlit-water-dashboard"}
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200 and response.json():
        result = response.json()[0]
        return float(result["lat"]), float(result["lon"])
    return None, None


for name in unique_places:
    lat, lon = geocode_place(name)
    print(f"{name} → {lat}, {lon}")
    geocoded[name] = {"lat": lat, "lon": lon}
    time.sleep(1)  # Respect rate limit

# Step 4: Merge back into original DataFrame
df["lat"] = df["CleanedName"].map(lambda x: geocoded.get(x, {}).get("lat"))
df["lon"] = df["CleanedName"].map(lambda x: geocoded.get(x, {}).get("lon"))

# Step 5: Save enriched dataset
output_file = "data/water_treatment_data_geocoded.csv"
df.to_csv(output_file, index=False)
print(f"Saved enriched data → {output_file}")
