from datetime import datetime, timedelta

import pandas as pd
import requests

# Define the API endpoint and query parameters
url = "https://api.existenz.ch/apiv1/hydro/daterange"

# end data is set to 5 years ago, utcnow() is deprecated
end_date = datetime.now() - timedelta(days=5*365)
start_date = datetime.now()
print("Fetching data from", end_date.strftime(
    '%Y-%m-%d'), "to", start_date.strftime('%Y-%m-%d'))
params = {
    "locations": "2099",
    "parameters": "flow",
    "enddate": end_date.strftime('%Y-%m-%d'),
    "startdate": start_date.strftime('%Y-%m-%d'),
    "app": "limmatFlow",
    "version": "0.0.1"
}

# Send the GET request
response = requests.get(url, params=params)
response.raise_for_status()  # Raise an error for bad responses

# Parse the JSON response
data = response.json()

# Extract relevant flow data
flow_data = [
    {
        "timestamp": datetime.utcfromtimestamp(entry["timestamp"]),
        "flow": entry["val"]
    }
    for entry in data.get("payload", []) if entry.get("par") == "flow"
]

# Create a DataFrame and save as CSV
df = pd.DataFrame(flow_data)
df.to_csv("flow_data_last_5_years.csv", index=False)
print("Saved data to flow_data_last_5_years.csv")
