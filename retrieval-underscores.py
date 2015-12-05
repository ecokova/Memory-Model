# -*- coding: utf-8 -*-
# Last Edited: 11.15.2015
#          By: Jen Hammelman
# COMP50 Concurrent Programming JEN_CHaZ Memory Model
# accesses API pydictionary for word associations

import threading
import random
import os
from collections import namedtuple

Association = namedtuple("MyStruct", "association frequency")

class Retrieval(threading.Thread):
    def __init__(self, STM, LTM, DONE, DONE_lock, wait_time):
        threading.Thread.__init__(self)
        self.LT = LTM
        self.ST = STM
        self.DONE = DONE
        self.wait_time = wait_time
        self.DONE_lock = DONE_lock
                
    def _parseAssoc(self, assoc):
        assoc_list = []
        start = False
        for i, line in enumerate(assoc):
            if '=>' in line:
                words = line.split()
                for word in words:
                    word = word.replace(',','')
                    if '=>' not in word:
                        assoc_list.append(word)
        return assoc_list

    def run(self):
        # while not self.DONE
        while not self.DONE[0]:
          #  self.DONE_lock.acquire()
          #  if self.DONE[0]:
          #      self.DONE_lock.release()
          #      break
          #  self.DONE_lock.release()
            # get a ST memory
            if self.ST.qsize() > 0:
                try:
                    i = random.randrange(0, self.ST.qsize())
                    ST_mem = self.ST.peek(i,True, self.wait_time)
                except:
                    continue
            # look for LT match to ST
                i = random.randrange(0, len(ST_mem.association))
                try:
                    retval = os.popen("wn {} -synsn".format(ST_mem.association[i]), "r")
                    assoc = retval.readlines()
                    ST_assocs = self._parseAssoc(assoc)
                    #print ST_assocs
                except:
                    continue
                for i in range(0, self.LT.qsize()):
                    try:
                        LT_mem = self.LT.peek(i, True, self.wait_time)
                    except Empty:
                        continue
                    # put my like-LT into ST
                try: 
                    if LT_mem.association[0] in ST_assocs:
                        self.ST.put(LT_mem)
                        break
                except UnboundLocalError:
                    continue
        
            
                        
