# dqn_agent.py
import torch
import torch.nn as nn
import torch.optim as optim
from torch.autograd import Variable
import numpy as np
from collections import deque
import random


class QNetwork(nn.Module):
    def __init__(self, input_size, output_size, hidden_size=64):
        super(QNetwork, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.fc3 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x

class ExperienceReplayBuffer:
    def __init__(self, capacity):
        self.capacity = capacity
        self.buffer = []

    def push(self, transition):
        if len(self.buffer) >= self.capacity:
            self.buffer.pop(0)
        self.buffer.append(transition)

    def sample(self, batch_size):
        return random.sample(self.buffer, batch_size)

    def __len__(self):
        return len(self.buffer)

class DQNAgent():
    def __init__(self, action_space, observation_space, hidden_size=64, learning_rate=1e-3, batch_size=64, gamma=0.99, buffer_size=10000, target_update_freq=500):
        super().__init__(action_space, observation_space)
        self.gamma = gamma
        self.batch_size = batch_size
        self.target_update_freq = target_update_freq
        self.num_actions = action_space.shape[0]
        self.num_states = observation_space.shape[0]

        self.q_network = QNetwork(self.num_states, self.num_actions, hidden_size)
        self.target_network = QNetwork(self.num_states, self.num_actions, hidden_size)
        self.target_network.load_state_dict(self.q_network.state_dict())
        self.target_network.eval()

        self.optimizer = optim.Adam(self.q_network.parameters(), lr=learning_rate)
        self.loss_function = nn.MSELoss()
        self.experience_replay = ExperienceReplayBuffer(buffer_size)
        self.update_count = 0

    def select_action(self, state, epsilon=0.1):
        if np.random.rand() < epsilon:
            return np.random.uniform(low=-1, high=1, size=self.num_actions)
        state = torch.from_numpy(state).float().unsqueeze(0)
        with torch.no_grad():
            q_values = self.q_network(state)
        return q_values.argmax(dim=1).item()

    def update(self):
        if len(self.experience_replay) < self.batch_size:
            return

        batch = self.experience_replay.sample(self.batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)

        states = torch.from_numpy(np.array(states)).float()
        actions = torch.from_numpy(np.array(actions)).float()
        rewards = torch.from_numpy(np.array(rewards)).float()
        next_states = torch.from_numpy(np.array(next_states)).float()
        dones = torch.from_numpy(np.array(dones)).float()

        q_values = self.q_network(states).gather(1, actions.long().unsqueeze(1)).squeeze()
        with torch.no_grad():
            next_q_values = self.target_network(next_states).max(dim=1)[0]
        target_q_values = rewards + self.gamma * next_q_values * (1 - dones)

        loss = self.loss_function(q_values, target_q_values)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        self.update_count += 1
        if self.update_count % self.target_update_freq == 0:
            self.target_network.load_state_dict(self.q_network.state_dict())

    def store_transition(self, state, action, reward, next_state, done):
        self.experience_replay.push((state, action, reward, next_state, done))

