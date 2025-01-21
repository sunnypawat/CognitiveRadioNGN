import numpy as np
from gnuradio import gr

class channel_selector(gr.sync_block):
    """
    A GNU Radio block for selecting the farthest free channel based on binary input states.
    """
    def __init__(self):
        gr.sync_block.__init__(self,
            name="channel_selector",
            in_sig=[(np.float32, 8)],  # Input: 8-channel binary states
            out_sig=[np.int32])       # Output: Selected channel index (0-7 or -1)

    def find_farthest_free_channel(self, state):
        """
        Finds the farthest free channel from all occupied ones.
        - state: A binary array of length 8 representing the channel states.
        - Returns the index of the farthest free channel, or -1 if no channels are free.
        """
        free_indices = np.where(state == 0)[0]
        occupied_indices = np.where(state == 1)[0]

        if len(free_indices) == 0:
            return -1  # No free channels

        # Calculate distances from each free channel to the nearest occupied channel
        distances = [
            min(abs(free_idx - occ_idx) for occ_idx in occupied_indices) if len(occupied_indices) > 0 else 8
            for free_idx in free_indices
        ]
        farthest_free_idx = free_indices[np.argmax(distances)]
        return farthest_free_idx

    def work(self, input_items, output_items):
        """
        Process incoming data and output the selected channel index.
        """
        X = input_items[0]  # Input data: shape (N, 8) for N samples of 8 channels
        output = []

        for row in X:
            selected_channel = self.find_farthest_free_channel(row)
            output.append(selected_channel)

        output_items[0][:] = output
        return len(output_items[0])
