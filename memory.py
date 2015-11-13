"""
Naomi Zarrilli
Comp 50 Project
Created 11/9/15
Edited 11/9/15
"""

import threading
import time


class MemoryThread(threading.Thread):
    def __init__(self, shared_mutex, max_size, DONE):
        threading.Thread = __init__(self)
        self.queue = Queue(max_size)
        self.mutex = shared_mutex
        self.DONE = DONE
    def run(self):
        start_time = time.time()
        while not self.DONE:
            if ((time.time - start_time) % 5.00 == 0):
                try:
                    self.queue.get()
                except Empty:
                    pass
