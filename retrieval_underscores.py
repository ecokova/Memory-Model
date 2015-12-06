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
    def __init__(self, STM, LTM, wait_time, DONE, myname):
        threading.Thread.__init__(self)
        self.LT = LTM
        self.ST = STM
        self.DONE = DONE
        self._wait_time = wait_time
        self._myname = myname
        
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
        runline = "wn {} -synsn"
        ST_mem = ""
        while (1):
            if self.DONE[0]:
                print self._myname
                return
            try: 
                ST_mem = self.ST.rand_peek(True, self._wait_time)
            except:
                continue
            # look for LT match to ST
            if ST_mem is "":
                continue
            try:
                retval = os.popen(runline.format(ST_mem.association[i]), "r")
                assoc = retval.readlines()
                ST_assocs = self._parseAssoc(assoc)
                #print ST_assocs
            except:
                continue
            try:
                LT_mem = self.LT.rand_peek(True, self._wait_time)
            except:
                continue
            # put my like-LT into ST
            try: 
                if LT_mem.association[0] in ST_assocs:
                    self.ST.put(LT_mem)
                    break
            except UnboundLocalError:
                continue
        
            
                        
