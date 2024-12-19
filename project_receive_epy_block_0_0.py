"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import csv


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, file_path="fft_output_t.csv", scale_factor=1e10):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Thereshold to readable (t)',   # will show up in GRC
            in_sig=[np.float32],
            out_sig=None
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.file_path = file_path
        
        self.file = open(self.file_path, 'w', newline='')
        self.write = csv.writer(self.file)
        self.file.write("FFT Data\n")
        self.scale_factor = scale_factor
        
    def work(self, input_items, output_items):
        """example: multiply with constant"""
        in_data = input_items[0] * self.scale_factor
        for value in in_data:
        	self.write.writerow([value])
        	
       	#self.file.write(str(input_items[0]))
       	return len(input_items[0])
