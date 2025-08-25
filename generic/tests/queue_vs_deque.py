"""deque is much faster than Queue."""

import os
import sys
from collections import deque
from queue import Queue

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from generic.timer import compare

q1 = Queue()
q2 = deque()

N = 1_000


def queue_():
    for i in range(N):
        q1.put((i, i))
        out = q1.get()


def deque_():
    for i in range(N):
        q2.append((i, i))
        out = q2.popleft()


if __name__ == "__main__":
    compare(
        [queue_, deque_],
        os.path.abspath(__file__),
        number=100,
        repeat=100,
    )
    # Raw medians:
    # queue_    0.123801
    # deque_    0.005663
    # dtype: float64

    # Scaled medians (relative to best):
    # queue_    21.795631
    # deque_     0.921096
    # dtype: float64
