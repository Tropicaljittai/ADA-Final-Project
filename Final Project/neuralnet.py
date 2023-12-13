import torch
from torch import nn
import torch.nn.functional as F
import numpy as np
from torch.optim import Adam
from torch.distributions.categorical import Categorical


class FeedForwardActorNuralNet(nn.Module):
    def __init__(self, n_actions, input_dims, alpha,fc1_dim=128, fc2_dim=128):
        super(FeedForwardActorNuralNet, self).__init__()

        self.actor = nn.Sequential(
            nn.Linear(*input_dims, fc1_dim),
            nn.ReLU(),
            nn.Linear(fc1_dim, fc2_dim),
            nn.ReLU(),
            nn.Linear(fc2_dim, n_actions),
            nn.Softmax(dim=-1)
        )

        self.optimizer = Adam(self.parameters(), lr=alpha)
    def forward(self, state):
        dist = self.actor(state)
        dist = Categorical(dist)

        return dist

class FeedForwardCriticNuralNet(nn.Module):
    def __init__(self, input_dims, alpha,fc1_dim=128, fc2_dim=128):
        super(FeedForwardCriticNuralNet, self).__init__()

        self.critic = nn.Sequential(
            nn.Linear(*input_dims, fc1_dim),
            nn.ReLU(),
            nn.Linear(fc1_dim, fc2_dim),
            nn.ReLU(),
            nn.Linear(fc2_dim, 1)
        )
        self.optimizer = Adam(self.parameters(), lr=alpha)
    def forward(self, state):
        value = self.critic(state)

        return value
