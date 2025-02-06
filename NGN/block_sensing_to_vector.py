"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import csv
import pmt


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block

    def __init__(self):  # only default arguments here
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block',   # will show up in GRC
            in_sig=[np.float32]*8,
            #out_sig=[(np.int32,8)]
            out_sig=None 
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).

        self.message_port_register_out(pmt.intern("out"))

    def work(self, input_items, output_items):
       	data = np.array(input_items)
       	
       	res = np.zeros(8, dtype=int)
       	for i in range(len(data)):
       		if np.any(data[i]):
       			res[i] = 1
       		else:
                        res[i] = 0
       				
       	#Integer message
       	#msg = pmt.cons(pmt.PMT_NIL, pmt.from_long(index))

       	msg = pmt.init_u32vector(len(res), res)
       	#print(msg)
        self.message_port_pub(pmt.intern("out"), msg)
        
        return len(input_items[0])
