import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# Load the real data, same as your linear regression script
df = pd.read_csv("../weather.csv")  # adjust path if needed
df["date"] = pd.to_datetime(df["date"])
df["temp_tomorrow"] = df["temp_max"].shift(-1)
df = df.dropna()

X = df[["temp_max", "temp_min", "precipitation", "windspeed"]].values
y = df["temp_tomorrow"].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

X_train_t = torch.tensor(X_train_scaled, dtype=torch.float32)
y_train_t = torch.tensor(y_train, dtype=torch.float32).view(-1, 1)
X_test_t = torch.tensor(X_test_scaled, dtype=torch.float32)
y_test_t = torch.tensor(y_test, dtype=torch.float32).view(-1, 1)

# THE NEW PART: actual neural net instead of plain nn.Linear
model = nn.Sequential(
    nn.Linear(4, 16),
    nn.ReLU(),
    nn.Linear(16, 1)
)

criterion = nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

epochs = 200
losses = []

for epoch in range(epochs):
    y_pred = model(X_train_t)
    loss = criterion(y_pred, y_train_t)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    losses.append(loss.item())

    if (epoch + 1) % 20 == 0:
        print(f"Epoch {epoch+1}/{epochs}, Loss: {loss.item():.4f}")

model.eval()
with torch.no_grad():
    y_pred_test = model(X_test_t)
    test_loss = criterion(y_pred_test, y_test_t)
    mae = torch.mean(torch.abs(y_pred_test - y_test_t))

print(f"\nTest MSE: {test_loss.item():.4f}")
print(f"Test MAE: {mae.item():.2f}°C")

plt.figure(figsize=(12, 5))
plt.plot(y_test, label="Actual", color="blue", alpha=0.7)
plt.plot(y_pred_test.numpy(), label="Predicted", color="red", alpha=0.7)
plt.title("Neural Net: Predicted vs Actual Tomorrow Temperature")
plt.legend()
plt.tight_layout()
plt.savefig("images/step10_neural_net_plot.png")
plt.show()