import requests
import pandas as pd

url = "https://archive-api.open-meteo.com/v1/archive"

params = {
    "latitude": 42.8864,
    "longitude": -78.8784,
    "start_date": "2022-01-01",
    "end_date": "2024-12-31",
    "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum", "windspeed_10m_max"],
    "timezone": "America/New_York"
}

response = requests.get(url, params=params)
data = response.json()

df = pd.DataFrame(data["daily"])
df.columns = ["date", "temp_max", "temp_min", "precipitation", "windspeed"]

print(df.head())
print(f"\nShape: {df.shape}")
print(f"\nData types:\n{df.dtypes}")

df.to_csv("weather.csv", index=False)