import torch
import torch.nn as nn

# LEARNED
# - Nueral Net: This is just a series of multiple linear equations and ReLU stacked on top of each other
#   to produce a dynamic final output
# 
# - ReLU (Rectified Linear Unit): Sets the output of a hinden layer of linear regeressions to max(0, res).
#   This is done so that in certain situations the final output equation will have some weights not active
#   and in others it will have those weights active. This leads to a final output that could be anything instead
#   of just linear. Without it, you would just get number x number x value and get a linear model. Think of ReLU 
#   as a on and off switch for certain predictors. There is no reason behind it beside the fact that it allows 
#   the model to train those layers while training the final output to be non-linear and more accurate
# 
# - Dead ReLU: This is when a hidden layer is trapped not being able to train out of always outputting a negative
#   number. It just so happend by chance that the equations gradient is stuck at 0 for outputing <=0 for all of 
#   the training data's inputs and now the gradient is also set to 0 by consequence, meaning it cannot improve.
# 

# OLD: one single linear layer (this was just linear regression)
old_model = nn.Linear(2, 1)

# NEW: two linear layers with something in between
new_model = nn.Sequential(
    nn.Linear(2, 4),   # 2 inputs -> 4 "hidden" numbers
    nn.ReLU(),         # the new piece - explained below
    nn.Linear(4, 1)    # 4 hidden numbers -> 1 final output
)

print(new_model)

x = torch.tensor([[10.0, 5.0]])
y_pred = new_model(x)
print("\nPrediction:", y_pred)