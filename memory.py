"""
Naomi Zarrilli
Comp 50 Project
Created 11/9/15
Edited 11/9/15
"""

import threading
import time
import FlexQueue 


class MemoryThread(threading.Thread):
    def __init__(self, shared_mutex, DONE, queue, wait_time):
        threading.Thread = super(MemoryThread, self).__init__()
        self.queue = queue
        self.mutex = shared_mutex
        self.DONE = DONE
        self.wait_time = wait_time
    def run(self):
        start_time = time.time()
        print start_time
        while not self.DONE:
            if ((time.time() - start_time) % self.wait_time == 0):
                try:
                    x = self.queue.get()
                    #print x
                except self.queue.Empty:
                    pass

#Testing
mutex = threading.Lock()
DONE = False
wait = .2
q = FlexQueue.FlexQueue(3)
q.put(1)
q.put(2)
q.put(3)
t = MemoryThread(mutex, DONE, q, wait)
t.run()
