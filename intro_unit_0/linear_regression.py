import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

# Load data
df = pd.read_csv("../weather.csv")
df["date"] = pd.to_datetime(df["date"])

# Create target: tomorrow's max temp
df["temp_tomorrow"] = df["temp_max"].shift(-1)
df = df.dropna()

# Features and target
X = df[["temp_max", "temp_min", "precipitation", "windspeed"]].values
y = df["temp_tomorrow"].values

# Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# Train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Absolute Error: {mae:.2f}°C")
print(f"R² Score: {r2:.2f}")
print(f"\nCoefficients:")
features = ["temp_max", "temp_min", "precipitation", "windspeed"]
for feature, coef in zip(features, model.coef_):
    print(f"  {feature}: {coef:.4f}")

# Plot predictions vs actual
plt.figure(figsize=(12, 5))
plt.plot(y_test, label="Actual", color="blue", alpha=0.7)
plt.plot(y_pred, label="Predicted", color="red", alpha=0.7)
plt.title("Linear Regression: Predicted vs Actual Tomorrow Temperature")
plt.legend()
plt.tight_layout()
plt.savefig("linear_regression_plot.png")
plt.show()