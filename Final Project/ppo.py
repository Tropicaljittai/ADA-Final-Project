
import torch
from torch.distributions import MultivariateNormal
from torch.optim import Adam
from neuralnet import FeedForwardNuralNet
class PPO:

    def __init__(self,env):
        self.hyperparameters()
        self.env = env
        self.observ_dim = env.observation_space.shape[0]
        self.act_dim = env.action_space.shape[0]

        # ALG STEP 1
        # Initialize actor and critic networks
        self.actor = FeedForwardNuralNet(self.observ_dim, self.act_dim)
        self.critic = FeedForwardNuralNet(self.observ_dim, 1)
        #adam optimazation
        self.actor_adam_optim = Adam(self.actor.parameters(), lr=self.learning_rate)
        #covariance matrix
        self.cov_var = torch.full(size=(self.act_dim,), fill_value=0.5)
        self.cov_mat = torch.diag(self.cov_var)


    def learn(self,totalSteps):
        current_tSteps = 0
        while current_tSteps < totalSteps:
            # ALG STEP 3
            batch_obs, batch_act, batch_logs, batch_rewardsTogo, batch_lens = self.dataRollout()

            V = self.evaluate(batch_obs, batch_act)
            Adv_K = batch_rewardsTogo - V.detach()
            Adv_K = (Adv_K - Adv_K.mean()) / (Adv_K.std() - 1e-10)

            for _ in range(self.n_updatePer_iteration):
                #  # Calculate pi_theta(a_t | s_t)
                _, curr_log_probs = self.evaluate(batch_obs, batch_act)
                #Calculate ratio
                ratio = torch.exp(curr_log_probs - batch_logs)
                #Calculate Surrogate losses
                srg1 = ratio*Adv_K
                srg2 = torch.clamp(ratio, 1 - self.clip, 1 + self.clip) * Adv_K

                actor_loss = (-torch.min(srg1,srg2)).mean()

                self.actor_adam_optim.zero_grad()
                actor_loss.backward()
                self.actor_adam_optim.step()

    def dataRollout(self):
        batch_obs = []
        batch_logs = []
        batch_act = []
        batch_rewards = []
        batch_rewardsTogo = []
        batch_lens = []
        t_steps = 0
        while t_steps < self.BatchTimeSteps:
            epsRewards = []
            obs = self.env.reset()
            isDone = False
            for eps_t in range(self.MaxTimeStepsPerEps):
                t_steps += 1
                batch_obs.append(obs)

                action,log_prob = self.get_action(obs)
                obs,rewards,isDone,_ = self.env.step(action)

                epsRewards.append(rewards)
                batch_act.append(action)
                batch_logs.append(log_prob)

                if isDone:
                    break
            batch_lens.append(eps_t + 1)
            batch_rewards.append(epsRewards)
        # Reshape data as tensors in the shape specified before returning
        batch_obs = torch.tensor(batch_obs, dtype=torch.float)
        batch_acts = torch.tensor(batch_act, dtype=torch.float)
        batch_logs = torch.tensor(batch_logs, dtype=torch.float)
        # ALG STEP #4
        batch_rewardsTogo = self.compute_rtgs(batch_rewards)
        # Return the batch data
        return batch_obs, batch_acts, batch_logs, batch_rewardsTogo, batch_lens

    def compute_rtgs(self, batch_rewards):
        # The rewards-to-go (rtg) per episode per batch to return.
        # The shape will be (num timesteps per episode)
        batch_rewardsTogo = []
        # Iterate through each episode backwards to maintain same order
        # in batch_rtgs
        for ep_rewards in reversed(batch_rewards):
            discounted_reward = 0  # The discounted reward so far
            for reward in reversed(ep_rewards):
                discounted_reward = reward + discounted_reward * self.gamma
                batch_rewardsTogo.insert(0, discounted_reward)
        # Convert the rewards-to-go into a tensor
        batch_rewardsTogo = torch.tensor(batch_rewardsTogo, dtype=torch.float)
        return batch_rewardsTogo
    def evaluate(self,batch_obs, batch_acts):
        V = self.critic(batch_obs).squeeze()
        # Calculate the log probabilities of batch actions using most
        # recent actor network.
        # This segment of code is similar to that in get_action()
        mean = self.actor(batch_obs)
        dist = MultivariateNormal(mean, self.cov_mat)
        log_probs = dist.log_prob(batch_acts)
        return V,log_probs
    def hyperparameters(self):
        self.BatchTimeSteps = 4800 #timesteps per batch
        self.MaxTimeStepsPerEps = 1600 #max timesteps per eps
        self.gamma = 0.95 #discount factir
        self.n_updatePer_iteration = 5
        self.clip = 0.2
        self.learning_rate = 0.005
