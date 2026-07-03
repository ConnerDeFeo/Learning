import torch
import torch.nn as nn

torch.manual_seed(0)  # so we get the same random numbers every time we run this

model = nn.Sequential(
    nn.Linear(1, 2),   # 1 input -> 2 hidden units
    nn.ReLU(),
    nn.Linear(2, 1)
)

optimizer = torch.optim.SGD(model.parameters(), lr=0.01)
criterion = nn.MSELoss()

# Simple made-up data: when x is small, answer is small. When x is big, answer is big.
x = torch.tensor([[1.0], [2.0], [8.0], [9.0]])
y_actual = torch.tensor([[2.0], [4.0], [16.0], [18.0]])

print("Hidden layer weights BEFORE training:")
print(model[0].weight)
print(model[0].bias)

for epoch in range(2000):
    y_pred = model(x)
    loss = criterion(y_pred, y_actual)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

print("\nHidden layer weights AFTER training:")
print(model[0].weight)
print(model[0].bias)

print("\nFinal predictions vs actual:")
print("Predicted:", model(x).detach().view(-1))
print("Actual:   ", y_actual.view(-1))