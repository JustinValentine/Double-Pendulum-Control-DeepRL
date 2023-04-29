import gymnasium as gym
import numpy as np
import random

# still need 
from dqn_agent import DQNAgent
from ppo_agent import PPOAgent
from a2c_agent import A2CAgent


def train_validate_test(agent, env, train_episodes, validation_episodes, test_episodes):
    training_rewards = []
    validation_rewards = []
    test_rewards = []
    
    for i in range(train_episodes + validation_episodes + test_episodes):
        state = env.reset()
        done = False
        episode_reward = 0
        
        while not done:
            action = agent.choose_action(state)
            next_state, reward, done, _ = env.step(action)
            episode_reward += reward
            
            if i < train_episodes:  # Training phase
                agent.train(state, action, reward, next_state, done)
            elif train_episodes <= i < (train_episodes + validation_episodes):  # Validation phase
                agent.validate(state, action, reward, next_state, done)
            else:  # Test phase
                agent.test(state, action, reward, next_state, done)
            
            state = next_state
        
        if i < train_episodes:
            training_rewards.append(episode_reward)
        elif train_episodes <= i < (train_episodes + validation_episodes):
            validation_rewards.append(episode_reward)
        else:
            test_rewards.append(episode_reward)
    
    return training_rewards, validation_rewards, test_rewards

# -- Initialize the environment and the agent -- 
env = gym.make('InvertedDoublePendulum-v4', render_mode="human")
state_dim = env.observation_space.shape[0]
action_dim = env.action_space.shape[0]
action_low = env.action_space.low
action_high = env.action_space.high

# Create instances of each agent
dqn_agent = DQNAgent(env.action_space, env.observation_space)
ppo_agent = PPOAgent(env.action_space, env.observation_space)
a2c_agent = A2CAgent(env.action_space, env.observation_space)

agent = dqn_agent 

# -- Set the number of episodes for training, validation, and testing -- 
train_episodes = 1000
validation_episodes = 200
test_episodes = 200

# -- Train, validate, and test the agent -- 
training_rewards, validation_rewards, test_rewards = train_validate_test(agent, env, train_episodes, validation_episodes, test_episodes)

# -- Analyze the results -- 
average_train_reward = np.mean(training_rewards)
average_validation_reward = np.mean(validation_rewards)
average_test_reward = np.mean(test_rewards)

print(f"Average Training Reward: {average_train_reward}")
print(f"Average Validation Reward: {average_validation_reward}")
print(f"Average Test Reward: {average_test_reward}")
