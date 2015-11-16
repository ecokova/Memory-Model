# Last Edited: 11.15.2015
#          By: Jen Hammelman
# COMP50 Concurrent Programming JEN_CHaZ Memory Model
# accesses API pydictionary for word associations

import threading
import random
from urllib2 import Request, urlopen, URLError

class Retrieval(threading.Thread):
    def __init__(self, ST_memBank, LT_memBank, DONE, waitTime)
        threading.Thread.__init__(self)
        self.LT = LT_memBank
        self.ST = ST_memBank
        self.DONE = DONE
        self.dictionary=PyDictionary()
        self.waitTime = waitTime

    def run(self):
        # while not self.DONE
        while not self.DONE:
            # get a ST memory
            i = random.randrange(0, self.ST.size())
            try:
                STmem = self.ST.peek(i,True, self.waitTime)
            except Empty:
                continue
            # look for LT match to ST
            request = Request("https://pydictionary-geekpradd.rhcloud"
                              ".com/api/translate/{}".format(STmem))
            try:
                response = urlopen(request)
                STassociations = response.read()
                for i in range(0, self.LT.size()):
                    try:
                        LTmem = self.LT.peek(i, True, self.waitTime)
                    except Empty:
                        continue
                    # put my like-LT into ST
                    if LTmem in STassociations:
                        self.STmem.put(LTmem)
                        break
            except URLError, e:
                continue


