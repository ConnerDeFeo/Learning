import torch

# A 2D tensor: think of this as 3 rows, 2 columns
# like 3 days of data, each with 2 features
# LEARNED: 
# - 2d tensor is just a bunch of individual data points that themselves have multiple peices of data
x_2d = torch.tensor([
    [10.0, 5.0],
    [12.0, 6.0],
    [8.0, 3.0]
])
print("2D tensor:")
print(x_2d)
print("Shape:", x_2d.shape)