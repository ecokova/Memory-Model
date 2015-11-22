'''
main.py
Jen Hammelman, Naomi Zarrilli, and Elena Cokova
Created 11/22/2015
Edited 11/22/2015
'''

import memory
import action
import retrieval
import FlexQueue
import threading
import sys
from collections import namedtuple
import time

Association = namedtuple("MyStruct", "association frequency")

def main(argv):
    DONE = [False]
    LTM = memory.MemoryThread(DONE, 0.2, 0)
    STM = memory.MemoryThread(DONE, 0.2, 7)
    SM  = memory.MemoryThread(DONE, 0.2, 5)
    RHS = action.Action(5,STM, LTM, 0.2, DONE)
    ATN = action.Action(0, SM, STM, 0.1, DONE)
    RTV = retrieval.Retrieval(STM.queue, LTM.queue, DONE, threading.Lock(), 0.2)
    threads = [LTM, STM, SM, RHS, ATN, RTV]
    for thread in threads:
        thread.start()
    with sys.stdin as f:
        for line in f:
            words = line.split()
            SM.queue.put(Association(words,0))
            time.sleep(0.2)
    f.close()
    DONE[0] = True
    for thread in threads:
        thread.join()
    print "Long Term Memory: ", list(LTM.queue.queue)
    print "Short Term Memory: ", list(STM.queue.queue)
    print "Sensory Memory: ", list(SM.queue.queue)
    exit(0)
    
if __name__ == '__main__':
    main(sys.argv)
