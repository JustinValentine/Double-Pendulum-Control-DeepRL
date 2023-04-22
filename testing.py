import gym
from dqn_agent import DQNAgent

env = gym.make('InvertedDoublePendulum-v4')
agent = DQNAgent(env.action_space, env.observation_space)

num_episodes = 1000
for episode in range(num_episodes):
    state = env.reset()
    done = False

    while not done:
        action = agent.select_action(state)
        next_state, reward, done, _ = env.step(action)
        agent.store_transition(state, action, reward, next_state, done)
        agent.update()
        state = next_state

    if episode % 10 == 0:
        print(f"Episode {episode} completed.")
