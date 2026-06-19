import torch
import torch.nn as nn

# LEARNED:
# - This is just taking the models prediction and finding the mean squared error or MSE
layer = nn.Linear(2, 1)

x = torch.tensor([[10.0, 5.0]])
y_actual = torch.tensor([[15.0]])  # let's say the real answer was 15.0

y_pred = layer(x)
print("Prediction:", y_pred)
print("Actual:", y_actual)

# Mean Squared Error: this is the same SS_res math from R^2 (Mean of actual point - predicted point square across all points)
criterion = nn.MSELoss()
loss = criterion(y_pred, y_actual)
print("Loss:", loss)