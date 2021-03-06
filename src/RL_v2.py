import argparse
from collections import Counter

import numpy as np
from itertools import count

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.distributions import Categorical

parser = argparse.ArgumentParser(description='PyTorch REINFORCE example')
parser.add_argument('--gamma', type=float, default=0.99, metavar='G',
                    help='discount factor (default: 0.99)')
parser.add_argument('--seed', type=int, default=543, metavar='N',
                    help='random seed (default: 543)')
parser.add_argument('--render', action='store_true',
                    help='render the environment')
parser.add_argument('--log-interval', type=int, default=10, metavar='N',
                    help='interval between training status logs (default: 10)')


args = parser.parse_args()


#
# env.seed(args.seed)
# torch.manual_seed(args.seed)
from global_ import cells
# Check PyTorch has access to MPS (Metal Performance Shader, Apple's GPU architecture)
torch.device = "mps" if torch.backends.mps.is_available() else "cpu"
print(f"Using device: {torch.device}")

class Policy(nn.Module):
    def __init__(self):
        super(Policy, self).__init__()
        self.input_n = len(cells)*2*3 + 2
        self.output_n = len(cells)*3+1
        self.affine1 = nn.Linear(self.input_n, 128)
        self.dropout = nn.Dropout(p=0.6)
        self.affine2 = nn.Linear(128, self.output_n)
        self.saved_log_probs = []
        self.rewards = []

    def forward(self, x):
        x = self.affine1(x)
        x = self.dropout(x)
        x = F.relu(x)
        action_scores = self.affine2(x)
        return F.softmax(action_scores, dim=1)


def select_action(state, in_policy):
    state = torch.from_numpy(state).float().unsqueeze(0)
    probs = in_policy(state)
    m = Categorical(probs)
    action = m.sample()
    in_policy.saved_log_probs.append(m.log_prob(action))
    return action.item()


def finish_episode():
    R = 0
    policy_loss = []
    returns = []  # sum of rewards
    for r in training_policy.rewards[::-1]:
        R = r + args.gamma * R  # gamma = 1
        returns.insert(0, R)
    returns = torch.tensor(returns)
    returns = (returns - returns.mean()) / (returns.std() + eps)
    for log_prob, R in zip(training_policy.saved_log_probs, returns):
        policy_loss.append(-log_prob * R)
    optimizer.zero_grad()
    policy_loss = torch.cat(policy_loss).sum()
    policy_loss.backward()
    optimizer.step()

    del training_policy.rewards[:]
    del training_policy.saved_log_probs[:]


training_policy = Policy()
optimizer = optim.Adam([
            {'params': training_policy.affine1.weight},
            {'params': training_policy.affine1.bias, 'lr': 1e-1}
            # {'params': training_policy.layer2.weight, 'lr': 0.001}
],  lr=1e-1)
eps = np.finfo(np.float32).eps.item()


def main():


    from sim_v3 import simulator

    print("0 policy avg score")
    av = 0
    # for i in range(20):
    #     A, X, total_reward, rewards_H, score = simulator(training_policy, 0)
    #     av += total_reward
    # av = av / 20
    running_reward = av
    # print(av)
    #
    # print("Random theta avg score")
    # av = 0
    # for i in range(20):
    #     A, X, total_reward, rewards_H, score = simulator(training_policy, 5)
    #     av += total_reward
    # av = av / 20
    # running_reward = av
    # print(av)

    for i_episode in range(100000):
        A, X, total_reward, rewards_H, score = simulator(training_policy, 5)
        training_policy.rewards = rewards_H

        running_reward = 0.05 * total_reward + (1 - 0.05) * running_reward
        finish_episode()

        if i_episode % 100 == 0:
            print('Episode {}\tLast reward: {:.2f}\tAverage reward: {:.2f} \t Score: {}'.format(
                i_episode, total_reward, running_reward, score))
            a_temp = [np.argmax(a_) for a_ in A]
            print(Counter(a_temp))
        if running_reward > 100:
            print("Solved! Running reward is now {} and "
                  "the last episode runs to time steps!".format(running_reward))
            break
        if i_episode % 500 == 0 and i_episode != 0:
            simulator(training_policy, 5, 180, print_state=True)
            avg = 0
            for i in range(30):
                A, X, total_reward, rewards_H, score = simulator(training_policy, 5, 180)
                avg += total_reward
            print(avg / 30)

if __name__ == '__main__':
    main()
