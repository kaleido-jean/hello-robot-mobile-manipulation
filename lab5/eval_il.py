import os
import torch
import numpy as np
import gymnasium as gym
from rl import TouchEnv
from pathlib import Path

# Setup Env
env = gym.make('TouchEnv', render_mode='human')

# Load Policy
policy_path = Path(__file__).parent / "imitation_policy.pt"
policy = torch.load(policy_path, weights_only=False)
policy.eval()

np.random.seed(None)
seed = np.random.randint(9000000)
# print(f"Seed: {seed}")
obs, info = env.reset(seed=seed)

terminated = False
truncated = False
while not terminated and not truncated:
    with torch.no_grad():
        action = policy(torch.Tensor(obs))

    obs, reward, terminated, truncated, info = env.step(action)
    # print(reward)

