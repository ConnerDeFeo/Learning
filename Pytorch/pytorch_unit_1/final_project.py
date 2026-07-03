import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import torch.nn as nn
import torch
from sklearn.preprocessing import StandardScaler

# Import the data
df = pd.read_csv("data/rochester_weather.csv")
df["date"] = pd.to_datetime(df["date"])

# Create the target value
df["windspeed_tomorrow"] = df["windspeed"].shift(-1)
df = df.dropna()

# Features and target
X = df[["temp_max", "temp_min", "precipitation", "windspeed"]].values
y = df["windspeed_tomorrow"].values

# Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# Model
model = LinearRegression()
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Absolute Error: {mae:.2f}kmh")
print(f"R² Score: {r2:.2f}")
print(f"\nCoefficients:")
features = ["temp_max", "temp_min", "precipitation", "windspeed"]
for feature, coef in zip(features, model.coef_):
    print(f"  {feature}: {coef:.4f}")
print("\n\n\n\n MOVING ONTO NUERAL NET")

# Setup data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

X_train_t = torch.tensor(X_train_scaled, dtype=torch.float32)
y_train_t = torch.tensor(y_train, dtype=torch.float32).view(-1, 1) # Make the representation of the data multiple rows instead of one row
X_test_t = torch.tensor(X_test_scaled, dtype=torch.float32)
y_test_t = torch.tensor(y_test, dtype=torch.float32).view(-1, 1)

# Build the nueral net
nueral_net = nn.Sequential(
    nn.Linear(4, 8),
    nn.ReLU(),
    nn.Linear(8, 1)
)

criterion = nn.MSELoss()
optimizer = torch.optim.SGD(nueral_net.parameters(), lr=0.01)

epochs = 200
losses = []

for epoch in range(epochs):
    y_pred = nueral_net(X_train_t) # get predictions for test data
    loss = criterion(y_pred, y_train_t) # find MSE

    optimizer.zero_grad() # make gradient 0
    loss.backward() # Find gradients for each weight
    optimizer.step() # adjust weights

    losses.append(loss.item()) # average

    if (epoch + 1) % 20 == 0:
        print(f"Epoch {epoch+1}/{epochs}, Loss: {loss.item():.4f}")

nueral_net.eval()
with torch.no_grad():
    y_pred_test = nueral_net(X_test_t) # check the final prediction
    test_loss = criterion(y_pred_test, y_test_t) # Find the final MSE
    mae = torch.mean(torch.abs(y_pred_test - y_test_t))
    r2 = r2_score(y_test_t, y_pred_test)

print(f"\nTest MSE: {test_loss.item():.4f}")
print(f"\nTest MAE: {mae.item():.2f}kmh")
print(f"\nTest R^2: {r2:.2f}")

plt.figure(figsize=(12, 5))
plt.plot(y_test, label="Actual", color="blue", alpha=0.7)
plt.plot(y_pred_test.numpy(), label="Predicted", color="red", alpha=0.7)
plt.title("Neural Net: Predicted vs Actual Windspeed Temperature")
plt.legend()
plt.tight_layout()
plt.savefig("images/final_image.png")
plt.show()