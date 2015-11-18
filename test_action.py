import action
import FlexQueue
import memory
import threading

from collections import namedtuple 

STLock = threading.Lock()
ST = memory.MemoryThread(STLock, False, FlexQueue.FlexQueue(), 1)
LTLock = threading.Lock()
LT = memory.MemoryThread(LTLock, False, FlexQueue.FlexQueue(), 1)
action = action.Action(5, ST, LT, 1, False)

Association = namedtuple("MyStruct", "association frequency")
m = Association(["dog", "good"], 1)


a = Association(["dog", "good"], 0)
ST.queue.put(a)
a = Association(["cat", "good"], 0)
ST.queue.put(a)
a = Association(["bird", "bad"], 0)
ST.queue.put(a)
a = Association(["horse", "good"], 0)
ST.queue.put(a)

a = Association(["blue", "good"], 0)
LT.queue.put(a)
a = Association(["orange", "bad"], 0)
LT.queue.put(a)
a = Association(["red", "bad"], 0)
LT.queue.put(a)
a = Association(["green", "good"], 0)
LT.queue.put(a)
print "Short term"
for i in range(0, ST.queue.qsize()):
        print ST.queue.peek(i)
print "Long term"
for i in range(0, LT.queue.qsize()):
        print LT.queue.peek(i)

action.run()

print "After action ran------------"

print "Short term"
for i in range(0, ST.queue.qsize()):
        print ST.queue.peek(i)
print "Long term"
for i in range(0, LT.queue.qsize()):
        print LT.queue.peek(i)
