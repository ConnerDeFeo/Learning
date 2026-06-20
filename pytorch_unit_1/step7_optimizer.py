import torch
import torch.nn as nn


# LEARNED:
# - To find a given gradient we need to look at the mean of (error1 x xi) for each weight.
#   for example, to find gradient w1, we would need the mean of (error_i X x1_i) so that larger
#   values effect the gradient more. Larger x value means more importance to the prediction
#   so the gradient must be larger to account. Take this and multiple by -2 to get the gradient 
#   for each weight
# - Next we need adjust the weights by using the learning formula wNew = wOld - (wGradient x learning rate)
#   After that the weights are updated, and this is the full cycle for machine learning
layer = nn.Linear(2, 1)

x = torch.tensor([[10.0, 5.0]])
y_actual = torch.tensor([[15.0]])

# The optimizer needs to know which numbers it's allowed to adjust (layer.parameters())
# and how big of a step to take each time (lr = learning rate)
optimizer = torch.optim.SGD(layer.parameters(), lr=0.01)

print("Weights BEFORE update:", layer.weight)
print("Bias BEFORE update:", layer.bias)

y_pred = layer(x)
criterion = nn.MSELoss()
loss = criterion(y_pred, y_actual)
print("\nLoss:", loss.item())

loss.backward()

# This is the new line. It applies the formula:
# w_new = w_old - lr * gradient
optimizer.step()

print("\nWeights AFTER update:", layer.weight)
print("Bias AFTER update:", layer.bias)