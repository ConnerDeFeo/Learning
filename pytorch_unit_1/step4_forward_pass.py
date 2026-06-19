import torch
import torch.nn as nn

# Same untrained layer as before
# LEARNED:
# - This is just passing the data through the models currently trained weights
# - Its just linear regression multiplying each number by the models weight
# - Pytorch saves how it calculated the number iun the output, this will be used so pytorch can trace back learn how to shift the weights
layer = nn.Linear(2, 1)
print("Weights:", layer.weight)
print("Bias:", layer.bias)

print()

# One single data point: 2 features, e.g. [temp_max, temp_min]
x = torch.tensor([[10.0, 5.0]])
print("Input:", x)

# Run it through the model - this is called the "forward pass"
y_pred = layer(x)
print("Prediction:", y_pred)