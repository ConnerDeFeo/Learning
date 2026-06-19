import torch
import torch.nn as nn

# LEARNED:
# - loss.backward() is the big function in pytorch that actually enables learning
# - Gradient: This is an array of numbers that are based on how wrong the models 
#   previous prediction were. The numbers give the direction and magnitude of 
#   adjustments that should happen to the weights to make them more accurate
#   based on the training data. For instance you may have -320 and 160. The 
#   The goal is to be as close to 0 as possible, as - means increae the weight
#   and + means decrease the given weight. However -380 would move the weight 
#   roughly twice as much as 160 would becasue it's weight is twice as large
# - Learning rate: The gradient numbers are not the exact amount the weight 
#   will move by, they are multiplied by a learning rate to slow down how 
#   much the model will actually change it's weights by
layer = nn.Linear(2, 1)

x = torch.tensor([[10.0, 5.0]])
y_actual = torch.tensor([[15.0]])

y_pred = layer(x)
criterion = nn.MSELoss()
loss = criterion(y_pred, y_actual)

print("Loss:", loss.item())
print()

print("Gradients BEFORE backward():")
print("Weight grad:", layer.weight.grad)
print("Bias grad:", layer.bias.grad)

# This is the new line. It calculates how much the loss would
# change if each weight changed slightly.
loss.backward()

print()
print("Gradients AFTER backward():")
print("Weight grad:", layer.weight.grad)
print("Bias grad:", layer.bias.grad)