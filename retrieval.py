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
    def __init__(self, ST_memBank, LT_memBank, DONE, DONElock, waitTime):
        threading.Thread.__init__(self)
        self.LT = LT_memBank
        self.ST = ST_memBank
        self.DONE = DONE
        self.waitTime = waitTime
        self.DONElock = DONElock
                
    def _parseAssoc(self, assoc):
        assocList = []
        start = False
        for i, line in enumerate(assoc):
            if '=>' in line:
                words = line.split()
                for word in words:
                    word = word.replace(',','')
                    if '=>' not in word:
                        assocList.append(word)
        return assocList

    def run(self):
        # while not self.DONE
        while not self.DONE[0]:
          #  self.DONElock.acquire()
          #  if self.DONE[0]:
          #      self.DONElock.release()
          #      break
          #  self.DONElock.release()
            # get a ST memory
            if self.ST.qsize() > 0:
                i = random.randrange(0, self.ST.qsize())
                try:
                    STmem = self.ST.peek(i,True, self.waitTime)
                except Empty:
                    continue
            # look for LT match to ST
                try:
                    retval = os.popen("wn {} -synsn".format(STmem.association[0]), "r")
                    assoc = retval.readlines()
                    STassociations = self._parseAssoc(assoc)
                    #print STassociations
                except:
                    continue
                for i in range(0, self.LT.qsize()):
                    try:
                        LTmem = self.LT.peek(i, True, self.waitTime)
                    except Empty:
                        continue
                    # put my like-LT into ST
                try: 
                    if LTmem.association[0] in STassociations:
                        self.ST.put(LTmem)
                        break
                except UnboundLocalError:
                    continue
        
            
                        
