import threading

class Action(threading.Thread):
        def __init__(self, threshold, from_memory, to_memory):
                thread.Thread.__init__(self)
                self._threshold = threshold
                self._association = {}
                self._from_memory = from_memory
                self._to_memory = to_memory

        # eg: Pay attention to, Rehearse, etc
        def performAction(self):
                i = 5 #some number

                # Gets value from _from_memory at given index (random or determined
                #       otherwise)
                self._association = self._from_memory.queue.peek(i) 
                # If the threshold is high enough to move the association, remove it
                #       from the current memory store
                if (self._association.frequency >= self._threshold):
                        self._from_memory.queue.remove(self._association)
                # If not, update the frequency and insert (replace) the association
                #       back in
                else:
                        self._association.frequency += 1
                        self._from_memory.queue.update(i,self._association)
                        self._association = {}
                
                # If the association was not reinserted, it needs to be moved to the 
                #       "to" memory store           
                if (self._association != {}):
                        self._to_memory.put(self._association)
                        self._association = {}