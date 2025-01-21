import numpy as np
from gnuradio import gr
import pmt

class channel_selector(gr.sync_block):
    """
    A GNU Radio block for selecting the farthest free channel based on binary input states
    and dynamically sending the center frequency via message passing.
    """
    def __init__(self, base_freq, channel_spacing):
        """
        Initialize the block with base frequency and channel spacing.

        Args:
        - base_freq: The base frequency for channel 0.
        - channel_spacing: The frequency spacing between adjacent channels.
        """
        gr.sync_block.__init__(self,
            name="channel_selector",
            in_sig=[(np.float32, 8)],  # Input: 8-channel binary states
            out_sig=[np.int32])       # Output: Selected channel index (0-7 or -1)

        self.base_freq = base_freq
        self.channel_spacing = channel_spacing

        # Declare a message output port for sending frequency updates
        self.message_port_register_out(pmt.intern("freq_update"))

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

    def send_center_freq_message(self, channel_index):
        """
        Sends a message with the center frequency based on the selected channel index.
        """
        if channel_index == -1:
            freq = None  # No valid channel selected
        else:
            freq = self.base_freq + channel_index * self.channel_spacing

        # Create a PMT pair with the key and value
        msg = pmt.cons(pmt.intern("center_freq"), pmt.from_double(freq if freq is not None else 0))
        self.message_port_pub(pmt.intern("freq_update"), msg)

    def work(self, input_items, output_items):
        """
        Process incoming data and output the selected channel index.
        """
        X = input_items[0]  # Input data: shape (N, 8) for N samples of 8 channels
        output = []

        for row in X:
            selected_channel = self.find_farthest_free_channel(row)
            self.send_center_freq_message(selected_channel)  # Send frequency message
            output.append(selected_channel)

        output_items[0][:] = output
        return len(output_items[0])
