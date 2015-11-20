import retrieval
import FlexQueue
import threading
import time

def main():
    LT = FlexQueue.FlexQueue()
    ST = FlexQueue.FlexQueue()
    DONE = list()
    insert = ["tasting", "cake", "is", "infinitely", "better", 
              "than", "eating", "dirt"]
    LTin = ["gossip", "ground", "soil", "earth", "baked", "dish"]
    for i in LTin:
        LT.put(i)
    DONE.append(False)
    DONElock = threading.Lock()
    print "Before thread initialization"
    thread = retrieval.Retrieval(ST, LT, DONE, DONElock,0)
    for i in insert:
        print "putting in short term", i
        ST.put(i)
    thread.start()
    time.sleep(7)
    DONElock.acquire()
    DONE[0] = True
    DONElock.release()
    thread.join()
    print "Longterm:", LT.queue
    print "Shortterm:", ST.queue

if __name__=="__main__":
    main()
