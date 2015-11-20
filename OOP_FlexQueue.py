from time import time as _time
try:
    import threading as _threading
except ImportError:
    import dummy_threading as _threading
from collections import deque
import heapq

class FlexQueue(Queue):
        def _peek(self, i):
        return self.queue[i]

        def _update(self, i, value):
        self.queue[i] = value

        def peek(self, i, block=True, timeout=None):
        self.not_empty.acquire()
        try:
            if not block:
                if i not in range(0, self._qsize()):
                    raise Empty
            elif timeout is None:
                while i not in range(0,self._qsize()):
                    self.not_empty.wait()
            elif timeout < 0:
                raise ValueError("'timeout' must be a non-negative number")
            else:
                endtime = _time() + timeout
                while i not in range(0, self._qsize()):
                    remaining = endtime - _time()
                    if remaining <= 0.0:
                        raise Empty
                    self.not_empty.wait(remaining)
            item = self._peek(i)
            return item
        finally:
            self.not_empty.release()

        def update(self, i, value, block=True, timeout=None):
            self.not_empty.acquire()
            try:
                if not block:
                    if i not in range(0,self._qsize()):
                        raise Empty
                elif timeout is None:
                    while i not in range(0, self._qsize()):
                        self.not_empty.wait()
                elif timeout < 0:
                    raise ValueError("'timeout' must be a non-negative number")
                else:
                    endtime = _time() + timeout
                    while i not in range(0, self._qsize()):
                        remaining = endtime - _time()
                        if remaining <= 0.0:
                            raise Empty
                        self.not_empty.wait(remaining)
                self._update(i,value)
            finally:
               self.not_empty.release()
