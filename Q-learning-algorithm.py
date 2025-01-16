import random

class ChannelSelector:
    def __init__(self):
        """
        Initializes weights (Q-values) for channels.
        Weights represent the value of selecting each channel.
        """
        self.weights = [0.0] * 8  # Assuming 8 channels
        self.learning_rate = 0.5   # Alpha: Controls how much new info overwrites old info
        self.discount_factor = 0.9 # Gamma: Importance of future rewards
        self.exploration_rate = 0.2  # Epsilon: Probability of random channel exploration

    def reward_function(self, channel_idx, occupied_indices):
        """
        Custom reward function:
        - Rewards channels farther from occupied ones.
        - Penalizes channels closer to occupied ones.
        """
        if not occupied_indices:
            return 10  # Maximum reward if no occupied channels exist

        # Calculate distance to the nearest occupied channel
        distance = min(abs(channel_idx - occ_idx) for occ_idx in occupied_indices)
        reward = distance ** 2  # Reward grows quadratically with distance
        return reward

    def update_weights(self, selected_channel, reward):
        """
        Update the Q-value (weight) for the selected channel based on reward.
        """
        old_value = self.weights[selected_channel]
        # Q-value update rule
        self.weights[selected_channel] += self.learning_rate * (reward - old_value)

    def find_farthest_free_channel(self, state):
        """
        Selects the best channel using Q-learning logic with exploration-exploitation.
        """
        free_indices = [idx for idx, val in enumerate(state) if val == 0]
        occupied_indices = [idx for idx, val in enumerate(state) if val == 1]

        if not free_indices:
            return -1  # No free channels

        # Exploration vs Exploitation
        if random.random() < self.exploration_rate:
            selected_channel = random.choice(free_indices)
        else:
            free_weights = [(idx, self.weights[idx]) for idx in free_indices]
            selected_channel = max(free_weights, key=lambda x: x[1])[0]

        # Reward calculation
        reward = self.reward_function(selected_channel, occupied_indices)
        self.update_weights(selected_channel, reward)

        return selected_channel

# Test scenarios
def test_selector():
    test_states = [
        [1, 0, 1, 0, 0, 0, 0, 1],  # Balanced occupancy
        [1, 1, 0, 0, 0, 0, 1, 1],  # Center is free
        [0, 0, 0, 0, 0, 0, 0, 0],  # All free
        [1, 1, 1, 1, 0, 1, 1, 1],  # Only one free
        [0, 1, 0, 1, 0, 1, 0, 1],  # Alternating pattern
        [1, 1, 1, 1, 1, 1, 0, 1],  # One free at the end
        [1, 0, 1, 1, 1, 0, 1, 1],  # Few scattered free
        [0, 0, 1, 1, 1, 1, 1, 0],  # Free at the edges
        [1, 1, 1, 0, 1, 1, 1, 1],  # Single free channel in the middle
        [0, 1, 1, 1, 1, 1, 1, 0],  # Only edges free
        [0, 1, 1, 0, 1, 1, 0, 1],  # Free channels in pairs
        [1, 0, 0, 0, 1, 1, 1, 1],  # Free block at the start
        [1, 1, 1, 1, 0, 0, 0, 0],  # Free block at the end
        [1, 0, 0, 1, 0, 0, 1, 0],  # Free channels scattered with gaps
        [1, 1, 0, 0, 0, 1, 1, 1],  # Free block in the center
        [0, 0, 1, 1, 0, 0, 1, 1],  # Two blocks of free channels
        [1, 1, 0, 0, 1, 1, 0, 0],  # Alternating blocks
        [1, 0, 1, 0, 1, 0, 1, 0],  # Alternating every other channel
        [0, 1, 0, 1, 0, 1, 0, 1],  # Alternating, starting with free
        [0, 0, 0, 1, 1, 0, 0, 0],  # Large free block with small gap
        [1, 0, 0, 0, 1, 0, 0, 0],  # Two free blocks separated by occupied
    ]

    selector = ChannelSelector()
    for i, state in enumerate(test_states):
        print(f"\nTest {i + 1}: State = {state}")
        for iteration in range(5):  # Run 5 iterations per state
            best_channel = selector.find_farthest_free_channel(state)
            print(f"Iteration {iteration + 1}: Best Channel = {best_channel}, Weights = {selector.weights}")
        selector.weights = [0.0] * 8  # Reset weights between tests

# Run the test
test_selector()
