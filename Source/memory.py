"""
Naomi Zarrilli
Comp 50 Project
Created 11/9/15
Edited 11/22/15
"""

import threading
import time
import FlexQueue 


class MemoryThread(threading.Thread):
    def __init__(self, DONE, wait_time, decay_rate, size_bound, myname):
        threading.Thread.__init__(self)
        self.queue = FlexQueue.FlexQueue(size_bound)
        self.DONE = DONE
        self._wait_time = wait_time
        self._myname = myname
        self._decay_rate = decay_rate
        
    def run(self):
        start_time = time.time()
        #print start_time
        while (1):
            if self.DONE[0]:
                return
            if ((time.time() - start_time) % self._decay_rate == 0):
                try:
                    x = self.queue.get(True, self._wait_time)
                except:
                    pass
