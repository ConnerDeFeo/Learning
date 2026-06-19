import torch.nn as nn

# Create a linear layer: 2 inputs, 1 output
# This represents: y = w1*x1 + w2*x2 + b
# LEARNED:
# - This is a untrained model taking in two inputs for predicting one output
# - Initially the model starts predicting with random weights and a random bais value, then improves
layer = nn.Linear(2, 1)

print("Weights:", layer.weight) # will be random if not assigned anything
print("Bias:", layer.bias)