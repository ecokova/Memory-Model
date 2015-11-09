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
                with self._from_memory.lock:
                        self._association = Queue.get(self._from_memory.queue) #get
                        if (self._association.frequency >= self._threshold):
                                Queue.remove(self._association)
                        else:
                                self._association.frequency += 1
                                Queue.put(self._association)
                                self._association = {}
                                
                if (self._association != {}):
                        with self._to_memory.lock:
                                Queue.put(self._association)
                        self._association = {}