import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.distributions import Categorical
import numpy as np

class ActorCriticNetwork(nn.Module):
    def __init__(self, n_inputs, n_actions, alpha):
        super(ActorCriticNetwork, self).__init__()
        self.fc1 = nn.Linear(16, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, 128)
        self.policy = nn.Linear(128, n_actions)
        self.value = nn.Linear(128, 1)
        self.optimizer = optim.Adam(self.parameters(), lr=alpha)

    def forward(self, state):
        x = F.relu(self.fc1(state))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        policy = self.policy(x)
        value = self.value(x)
        return policy, value

class PPOMemory:
    def __init__(self, batch_size):
        self.states = []
        self.probs = []
        self.vals = []
        self.actions = []
        self.rewards = []
        self.dones = []
        self.batch_size = batch_size

    def generate_batches(self):
        n_states = len(self.states)
        batch_start = np.arange(0, n_states, self.batch_size)
        indices = np.arange(n_states, dtype=np.int64)
        np.random.shuffle(indices)
        batches = [indices[i:i+self.batch_size] for i in batch_start]
        return np.array(self.states), np.array(self.actions), np.array(self.probs), np.array(self.vals), np.array(self.rewards), np.array(self.dones), batches

    def store_memory(self, state, action, probs, vals, reward, done):
        self.states.append(state)
        self.actions.append(action)
        self.probs.append(probs)
        self.vals.append(vals)
        self.rewards.append(reward)
        self.dones.append(done)

    def clear_memory(self):
        self.states = []
        self.actions = []
        self.probs = []
        self.vals = []
        self.rewards = []
        self.dones = []

class Agent:
    def __init__(self, n_inputs, n_actions, alpha, gamma=0.99, gae_lambda=0.95, policy_clip=0.2, n_epochs=4, batch_size=64):
        self.gamma = gamma
        self.policy_clip = policy_clip
        self.n_epochs = n_epochs
        self.gae_lambda = gae_lambda
        self.memory = PPOMemory(batch_size)
        self.actor_critic = ActorCriticNetwork(n_inputs, n_actions, alpha)

    def choose_action(self, observation):
        state = torch.tensor([observation], dtype=torch.float)
        probabilities, _ = self.actor_critic.forward(state)
        probabilities = F.softmax(probabilities, dim=1)
        action_probs = Categorical(probabilities)
        action = action_probs.sample()
        log_probs = action_probs.log_prob(action)
        return action.item(), log_probs

    def calculate_returns(self, rewards, dones, values):
        returns = []
        gae = 0  # Generalized Advantage Estimation
        for step in reversed(range(len(rewards))):
            delta = rewards[step] + self.gamma * values[step + 1] * (1 - int(dones[step])) - values[step]
            gae = delta + self.gamma * self.gae_lambda * (1 - int(dones[step])) * gae
            returns.insert(0, gae + values[step])
        return returns

    def learn(self):
        for _ in range(self.n_epochs):
            state_arr, action_arr, old_prob_arr, vals_arr, reward_arr, dones_arr, batches = self.memory.generate_batches()

            values = vals_arr + [0]  # Append a dummy 0 for terminal state

            returns = self.calculate_returns(reward_arr, dones_arr, values)

            for batch in batches:
                states = torch.tensor(state_arr[batch], dtype=torch.float)
                old_probs = torch.tensor(old_prob_arr[batch])
                actions = torch.tensor(action_arr[batch])
                returns_batch = torch.tensor(returns[batch])

                probabilities, values = self.actor_critic.forward(states)
                probabilities = F.softmax(probabilities, dim=1)
                critic_values = values.squeeze()

                new_probs = probabilities.gather(1, actions.unsqueeze(1)).squeeze(1)
                prob_ratio = new_probs.exp() / old_probs.exp()
                weighted_probs = prob_ratio * returns_batch
                clipped_probs = torch.clamp(prob_ratio, 1-self.policy_clip, 1+self.policy_clip) * returns_batch
                actor_loss = -torch.min(weighted_probs, clipped_probs).mean()

                returns_batch = returns_batch.detach()
                critic_loss = F.mse_loss(critic_values, returns_batch)

                total_loss = actor_loss + 0.5 * critic_loss
                self.actor_critic.optimizer.zero_grad()
                total_loss.backward()
                self.actor_critic.optimizer.step()

        self.memory.clear_memory()
