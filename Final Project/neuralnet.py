import os
import torch as T
from torch import nn
import torch.nn.functional as F
import numpy as np
from torch.optim import Adam
from torch.distributions.categorical import Categorical


class FeedForwardActorNuralNet(nn.Module):

    def __init__(self, n_actions, input_dims, alpha,fc1_dim=128, fc2_dim=128,chkpt_dir='tmp/ppo'):
        super(FeedForwardActorNuralNet, self).__init__()
        self.checkpoint_file = os.path.join(chkpt_dir, 'actor_torch_ppo')
        input_dim = np.prod(*input_dims)

        self.actor = nn.Sequential(
            nn.Linear(input_dim, fc1_dim),
            nn.ReLU(),
            nn.Linear(fc1_dim, fc2_dim),
            nn.ReLU(),
            nn.Linear(fc2_dim, n_actions),
            nn.Softmax(dim=-1)
        )

        self.optimizer = Adam(self.parameters(), lr=alpha)
        self.device = T.device('cuda:0' if T.cuda.is_available() else 'cpu')
        self.to(self.device)
    def forward(self, state):
        dist = self.actor(state)
        dist = Categorical(dist)

        return dist
    def save_checkpoint(self):
        T.save(self.state_dict(), self.checkpoint_file)

    def load_checkpoint(self):
        self.load_state_dict(T.load(self.checkpoint_file))

class FeedForwardCriticNuralNet(nn.Module):
    def __init__(self, input_dims, alpha,fc1_dim=128, fc2_dim=128,chkpt_dir='tmp/ppo'):
        super(FeedForwardCriticNuralNet, self).__init__()
        self.checkpoint_file = os.path.join(chkpt_dir, 'critic_torch_ppo')
        input_dim = np.prod(*input_dims)

        self.critic = nn.Sequential(
            nn.Linear(input_dim, fc1_dim),
            nn.ReLU(),
            nn.Linear(fc1_dim, fc2_dim),
            nn.ReLU(),
            nn.Linear(fc2_dim, 1)
        )
        self.optimizer = Adam(self.parameters(), lr=alpha)
        self.device = T.device('cuda:0' if T.cuda.is_available() else 'cpu')
        self.to(self.device)
    def forward(self, state):
        value = self.critic(state)

        return value
    def save_checkpoint(self):
        T.save(self.state_dict(), self.checkpoint_file)

    def load_checkpoint(self):
        self.load_state_dict(T.load(self.checkpoint_file))