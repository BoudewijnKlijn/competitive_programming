import heapq
import os
import random
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from generic.timer import compare

N = 10_000


def heapify_():
    nums = [random.randint(0, N) for _ in range(N)]
    heapq.heapify(nums)


def loop_heappush():
    nums = [random.randint(0, N) for _ in range(N)]
    new = list()
    for n in nums:
        heapq.heappush(new, n)


def setup_cost():
    nums = [random.randint(0, N) for _ in range(N)]


if __name__ == "__main__":
    compare(
        [heapify_, loop_heappush, setup_cost],
        os.path.abspath(__file__),
        number=10,
        repeat=100,
    )
