from gnuradio import gr
import pmt
import numpy as np
import random
import time

class ChannelSelector:
    def __init__(self):
        self.weights = [0.0] * 8  # Assuming 8 channels
        self.learning_rate = 0.5   # Alpha: Controls how much new info overwrites old info
        self.discount_factor = 0.5 # Gamma: Importance of future rewards
        self.exploration_rate = 0.1  # Epsilon: Probability of random channel exploration

    def reward_function(self, channel_idx, occupied_indices):
        if not occupied_indices:
            return 10

        # Calculate distance to the nearest occupied channel
        distance = min(abs(channel_idx - occ_idx) for occ_idx in occupied_indices)
        reward = distance ** 2  # Reward grows with distance
        return reward

    def update_weights(self, selected_channel, reward):
        old_value = self.weights[selected_channel]
        self.weights[selected_channel] += self.learning_rate * (reward - old_value)

    def find_farthest_free_channel(self, state):
        """
        Selects the best channel using Q-learning logic with exploration-exploitation.
        - state: A list or array of length 8 with binary values (0: free, 1: occupied)
        """
        free_indices = [idx for idx, val in enumerate(state) if val == 0]
        occupied_indices = [idx for idx, val in enumerate(state) if val == 1]

        if not free_indices:
            return -1  # No free channels

        if random.random() < self.exploration_rate:
            selected_channel = random.choice(free_indices)
        else:
            free_weights = [(idx, self.weights[idx]) for idx in free_indices]
            selected_channel = max(free_weights, key=lambda x: x[1])[0]

        reward = self.reward_function(selected_channel, occupied_indices)
        self.update_weights(selected_channel, reward)

        return selected_channel

class channel_selector(gr.sync_block):
    """
    A GNU Radio block for selecting the farthest free channel based on binary input states
    and dynamically sending the center frequency via message passing.
    """
    def __init__(self, base_freq=2.4e9, channel_spacing=1e6):
        """
        Args:
        - base_freq: The base frequency for channel 0.
        - channel_spacing: The frequency spacing between adjacent channels.
        """
        gr.sync_block.__init__(self,
            name="channel_selector",
            in_sig=None,
            #in_sig=[(np.int32, 8)],  # Input: 8-channel binary states
            out_sig=None
        )
        self.message_port_register_in(pmt.intern("out"))
        self.set_msg_handler(pmt.intern("out"),self.handle_msg)
        self.channels = []
        self.msg = 0

        self.base_freq = base_freq
        self.channel_spacing = channel_spacing

        # Instantiate the enhanced Q-learning channel selector
        self.selector = ChannelSelector()

        # Declare a message output port for sending frequency updates
        self.message_port_register_out(pmt.intern("freq"))
        self.farthest_free_index = 0
        
    def find_farthest_free_channel(self, state):
        """
        Finds the farthest free channel using the integrated Q-learning logic.
        - state: A binary array of length 8 representing the channel states.
        - Returns the index of the farthest free channel, or -1 if no channels are free.
        """
        return self.selector.find_farthest_free_channel(state)

    def send_center_freq_message(self, channel_index, gain, text):
        """
        Sends a message with the center frequency based on the selected channel index.
        """
        if channel_index == -1:
            freq = 0  # Default to 0 if no valid channel is selected
        else:
            freq = self.base_freq + channel_index * self.channel_spacing

        msg = pmt.make_dict()
        msg = pmt.dict_add(msg, pmt.intern("freq"), pmt.from_double(freq))
        msg = pmt.dict_add(msg, pmt.intern("gain"), pmt.from_double(gain))
        msg = pmt.dict_add(msg, pmt.intern("Note"), pmt.string_to_symbol(text))
        self.message_port_pub(pmt.intern("freq"), msg)

    def handle_msg(self, msg):

        self.channels = pmt.u32vector_elements(msg)
        current_state = self.channels
        self.farthest_free_index = self.find_farthest_free_channel(current_state)
        
        self.msg += 1
        #print(self.msg)
        
        if self.msg == 2000:
            self.send_center_freq_message(self.farthest_free_index, 0, "Sensing")
        
        if self.msg == 3000:
            print(current_state)

            print("Transmitting at:", self.farthest_free_index)
            self.send_center_freq_message(self.farthest_free_index, 80, "Transmitting")
            self.msg = 0

