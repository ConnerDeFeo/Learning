import torch
import torch.nn as nn

# LEARED:
# - Loop the training sequence over and over to make the model more accurate
# - The rate that it learns decreases as it gets more accurtae becasue the gradient gets smaller
layer = nn.Linear(2, 1)
optimizer = torch.optim.SGD(layer.parameters(), lr=0.01)
criterion = nn.MSELoss()

x = torch.tensor([[10.0, 5.0], [4.0, 2.0]])
y_actual = torch.tensor([[15.0], [8.0]])

print("Weights BEFORE training:", layer.weight)
print("Bias BEFORE training:", layer.bias)
print()

# This is the new part: doing the same 4 steps over and over
for epoch in range(10):
    y_pred = layer(x)
    loss = criterion(y_pred, y_actual)

    optimizer.zero_grad()  # clear old gradients before computing new ones
    loss.backward()
    optimizer.step()

    print(f"Epoch {epoch+1}: Loss = {loss.item():.4f}")

print()
print("Weights AFTER training:", layer.weight)
print("Bias AFTER training:", layer.bias)