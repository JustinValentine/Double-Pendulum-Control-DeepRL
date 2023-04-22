import gymnasium as gym

env = gym.make('InvertedDoublePendulum-v4', render_mode="human")

# Reset the environment to the initial state
state = env.reset()

# Set the number of time steps to visualize
num_timesteps = 2000

# Visualize the environment
for _ in range(num_timesteps):
    env.render()  # Render the current state of the environment
    action = env.action_space.sample()  # Sample a random action from the action space
    state, reward, done, info, _ = env.step(action)  # Take a step using the sampled action

    if done:  # If the episode is terminated, reset the environment
        state = env.reset()

# Close the environment
env.close()