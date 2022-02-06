# AOC learnings

## regex
? for 0 or 1 match
(...) to match a group

## use instead of class, because you get init and repr for free
from dataclasses import dataclass 

## use assert to test sample data

## use type hinting immediately

## use debugging tools better

## use cycle to repeat iterating that iterator/iterable
from itertools import cycle

## BFS even though i didn't know it was BFS

## queue.Queue, queue.SimpleQueue, PriorityQueue
use:
d = Queue()
d.put(1)
d.get(2)
d.empty() # return true if empty
d.full() # returns true if full


## itertools.count
- can be used instead of while. removes the need to increase a variable since it is done by the function

 itertools.count(start=0, step=1)

    Make an iterator that returns evenly spaced values starting with number start. Often used as an argument to map() to generate consecutive data points. Also, used with zip() to add sequence numbers. Roughly equivalent to:

    def count(start=0, step=1):
        # count(10) --> 10 11 12 13 14 ...
        # count(2.5, 0.5) -> 2.5 3.0 3.5 ...
        n = start
        while True:
            yield n
            n += step

## local and global variables
- safest to use only local


## coordinate compression (TODO)

## print with separator
print(*a, sep='...')
