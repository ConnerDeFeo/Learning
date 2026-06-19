import torch

# A tensor is just PyTorch's version of an array, almost identical to numpy
# LEARNED:
# - Tensors: They are just arrays that can run on the GPU and handle gradients
x = torch.tensor([1.0, 2.0, 3.0])
print(x)
print(type(x))
print(x.shape)