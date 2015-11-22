import threading
import random
from collections import namedtuple

## Struct format and example:
Association = namedtuple("MyStruct", "association frequency")
## m = Association(["dog", "good"], 1)

class Action(threading.Thread):
        def __init__(self, threshold, from_memory, to_memory, wait_time, DONE):
                threading.Thread.__init__(self)
                self._threshold = threshold
                self._association = []
                self._from_memory = from_memory
                self._to_memory = to_memory
                self._wait_time = wait_time
                self.DONE = DONE

        def run(self):
                i = 0
                while not self.DONE:
                        self.performAction()
                        i = i + 1
                        self.DONE = (i == 100)
        # eg: Pay attention to, Rehearse, etc
        def performAction(self): 
                if (self._from_memory.queue.qsize() < 1):
                        return
                i = random.randrange(0, self._from_memory.queue.qsize())

                # Gets value from _from_memory at given index (random or determined
                #       otherwise)
                try:
                        self._association = self._from_memory.queue.peek(i) 
                except:
                        return
                # If the threshold is high enough to move the association, remove it
                #       from the current memory store
                if (self._association.frequency >= self._threshold):
                        self._from_memory.queue.remove(self._association)
                # If not, update the frequency and insert (replace) the association
                #       back in
                else:
                        self._association = Association(self._association.association, self._association.frequency + 1)
                        self._from_memory.queue.update(i,self._association)
                        self._association = []
                
                # If the association was not reinserted, it needs to be moved to the 
                #       "to" memory store           
                if (self._association != []):
                        self._to_memory.queue.put(self._association)
                        self._association = []