import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("weather.csv")
df["date"] = pd.to_datetime(df["date"])

fig, axes = plt.subplots(3, 1, figsize=(12, 10))

# Plot 1: Temperature
axes[0].plot(df["date"], df["temp_max"], color="red", label="Max Temp")
axes[0].plot(df["date"], df["temp_min"], color="blue", label="Min Temp")
axes[0].set_title("Daily Temperature (°C)")
axes[0].legend()

# Plot 2: Precipitation
axes[1].bar(df["date"], df["precipitation"], color="steelblue", label="Precipitation")
axes[1].set_title("Daily Precipitation (mm)")
axes[1].legend()

# Plot 3: Wind Speed
axes[2].plot(df["date"], df["windspeed"], color="green", label="Wind Speed")
axes[2].set_title("Daily Wind Speed (km/h)")
axes[2].legend()

plt.tight_layout()
plt.savefig("weather_plot.png")
plt.show()
print("Plot saved to weather_plot.png")