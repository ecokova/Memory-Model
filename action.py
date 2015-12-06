# -*- coding: utf-8 -*-
import threading
import random
from collections import namedtuple

## Struct format and example:
Association = namedtuple("MyStruct", "association frequency")


class Action(threading.Thread):
        def __init__(self, threshold, from_memory, to_memory, wait_time, DONE, myname):
                threading.Thread.__init__(self)
                self._threshold = threshold
                self._association = None
                self._from_memory = from_memory
                self._to_memory = to_memory
                self._wait_time = wait_time
                self.DONE = DONE
                self._myname = myname

	def run(self):
     		while (1):
             		if self.DONE[0]:
                    		 print self._myname
                                 return
                        i = 0
             		# Gets value from _from_memory at random index
             		try:
                    		 self._association,i = self._from_memory.rand_peek(True, self._wait_time)
             		except:
                                 print "peek failed"
                                 continue
                        # If the threshold is high enough to move the association, remove it
                        #       from the current memory store
                        print "past peek"
             		if (self._association.frequency >= self._threshold):
                   		  try:
                            		 self._from_memory.remove(self._association, True, self._wait_time)
                                  except:
                            		 pass
                        # If not, update the frequency and insert (replace) the association
                        #       back in
                        else:
                    		 self._association = Association(self._association.association,
                            		                         self._association.frequency + 1)
                                 self._from_memory.update(i,self._association, True, self._wait_time)

                    		 self._association = None

                        # If the association was not reinserted, it needs to be moved to the 
                        #       "to" memory store           
                        if (self._association != None):
                    		 try:
                                        print "successful update"
                     		        self._to_memory.put(self._association, True, self._wait_time)
                    		 except:
                            		 pass
                                 self._association = None
