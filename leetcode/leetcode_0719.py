import heapq
import timeit
import tracemalloc
from collections import Counter, deque
from itertools import combinations, repeat
from typing import List

import numpy as np


class Solution:
    def smallestDistancePair(self, nums: List[int], k: int) -> int:
        """If len(nums) == N, then N*(N-1)/2 distances need to be calculated.
        Assuming I sort nums beforehand.
        I can visualize as an upper triangular matrix.
        Where distance at r, c nums[c] - nums[r] if r < c.
        The distances in the rows and columns are in non-decreasing order.
        Rows have lowest left. Columns have lowest at bottom.
        With generators I can prevent big memory usage.
        As well as with a frontier (only check distances of frontier cells)."""
        # return self.dict_deque(nums, k)
        return self.generator_counter(nums, k)

    @staticmethod
    def naive(nums, k):
        """Memory limited exceeded. Not fast.
        18/19 passed."""
        distance = []
        for i, num1 in enumerate(nums[:-1]):
            for num2 in nums[i + 1 :]:
                distance.append(abs(num1 - num2))
        distance.sort()
        return distance[k - 1]

    @staticmethod
    def generator_sorted(nums, k):
        """Memory limit exceeded. Similar speed as naive.
        18/19 passed."""
        nums.sort()
        return sorted(b - a for a, b in combinations(nums, 2))[k - 1]

    @staticmethod
    def generator_counter(nums, k):
        """Time limit exceeded.
        18/19 passed.
        Slightly slower than naive.
        Should have lower memory because diffs stored in Counter."""
        nums.sort()
        c = Counter(b - a for a, b in combinations(nums, 2))
        for diff, count in sorted(c.items()):
            if count >= k:
                return diff
            k -= count

    @staticmethod
    def frontier_heapq(nums, k):
        """Time limit exceeded instead of Memory limit exceeded.
        Still slow but uses less memory.
        Only stores differences of numbers that are at frontier
        Using insert order as secondary key makes it slower."""
        nums.sort()
        diff = [
            # (nc - nr, -k, r, c)   # delta, insert_order, r, c
            (nc - nr, r, c)
            for r, c, nr, nc in zip(
                range(len(nums)), range(1, len(nums)), nums, nums[1:]
            )
        ]
        heapq.heapify(diff)
        q = deque()
        furthest_col_in_row = [r + 1 for r in range(len(nums) - 1)]  # frontier
        while k > 1:
            k -= 1
            # use deque to perform more efficient heappushpop operation than separate heappush and heappop
            if q:
                *_, r, c = heapq.heappushpop(diff, q.popleft())
            else:
                *_, r, c = heapq.heappop(diff)

            furthest_col_in_row[r] = c + 1

            # check where frontier is in row above. if above, then we can add that cell to heap
            if r > 0 and furthest_col_in_row[r - 1] >= c:
                # q.append((nums[c] - nums[r - 1], -k, r - 1, c))
                q.append((nums[c] - nums[r - 1], r - 1, c))

            # check where frontier is in row below. if 2 further to right, then we can add that cell to heap
            if r < len(nums) - 2 and furthest_col_in_row[r + 1] >= c + 2:
                # q.append((nums[c + 1] - nums[r], -k, r, c + 1))
                q.append((nums[c + 1] - nums[r], r, c + 1))

        if not diff and q:
            return q[0][0]
        elif diff and not q:
            return diff[0][0]
        else:
            return min(diff[0][0], q[0][0])

    @staticmethod
    def generator_heapq(nums, k):
        """Slowwww"""
        nums.sort()
        return heapq.nsmallest(k, (b - a for a, b in combinations(nums, 2)))[-1]

    @staticmethod
    def frontier_dict(nums, k):
        """Use dict with deques instead of heapq.
        Still using frontier, so low memory usage, but faster than heapq."""
        nums.sort()

        diffs = dict()
        for r, c, nr, nc in zip(range(len(nums)), range(1, len(nums)), nums, nums[1:]):
            delta = nc - nr
            try:
                diffs[delta].append((r, c))
            except KeyError:
                diffs[delta] = deque([(r, c)])

        minimum = min(diffs)
        furthest_col_in_row = [r + 1 for r in range(len(nums) - 1)]  # frontier
        while k > 1:
            k -= 1
            try:
                r, c = diffs[minimum].popleft()
            except IndexError:
                del diffs[minimum]
                minimum = min(diffs)
                r, c = diffs[minimum].popleft()

            furthest_col_in_row[r] = c + 1

            # check where frontier is in row above. if above, then we can add that cell
            if r > 0 and furthest_col_in_row[r - 1] >= c:
                delta = nums[c] - nums[r - 1]
                try:
                    diffs[delta].append((r - 1, c))
                except KeyError:
                    diffs[delta] = deque([(r - 1, c)])

            # check where frontier is in row below. if 2 further to right, then we can add that cell
            if r < len(nums) - 2 and furthest_col_in_row[r + 1] >= c + 2:
                delta = nums[c + 1] - nums[r]
                try:
                    diffs[delta].append((r, c + 1))
                except KeyError:
                    diffs[delta] = deque([(r, c + 1)])

            if len(diffs[minimum]) == 0:
                del diffs[minimum]
                minimum = min(diffs)

        return minimum


def file_to_list_int(filename):
    return list(map(int, open(filename).read().split(",")))


# Timings

import pandas as pd
from tabulate import tabulate

s = Solution()
stats = pd.DataFrame()
params = [
    ([1, 3, 1], 1),
    ([1, 1, 1], 2),
    ([1, 6, 1], 3),
    ([9, 10, 7, 10, 6, 1, 5, 4, 9, 8], 18),
    ([38, 33, 57, 65, 13, 2, 86, 75, 4, 56], 26),
    *[
        (file_to_list_int(file), k)
        for file, k in zip(
            [
                "nums_0719_0.txt",
                "nums_0719_1.txt",
                "nums_0719_2.txt",
            ],
            repeat(25_000_000),
        )
    ],
]
answers = [
    0,
    0,
    5,
    2,
    36,
    1,
    292051,
    3,
]
# assert len(params) == len(answers)
funcs = [func for func in dir(Solution) if not func.startswith("__")]
track_memory = False  # tracking memory usage makes frontier extremely slow
for f in funcs:
    print(f"\nRunning {f}")
    if f == "smallestDistancePair":
        continue

    runtimes = []
    memories = []
    for i, (p, a) in enumerate(zip(params, answers)):
        print(f"{i}", end=", ")

        if track_memory:
            tracemalloc.start()

        method = getattr(s, f)
        ans = method(*p)
        assert ans == a, f"{f}: {ans} != {a}"
        runtime = timeit.timeit("method(*p)", globals=globals(), number=1)

        runtimes.append(runtime)
        if track_memory:
            peak = tracemalloc.get_traced_memory()[1]
            tracemalloc.stop()
            memories.append(peak)
        else:
            memories.append(np.nan)

    stats = pd.concat(
        (stats, pd.Series(data=runtimes, name=f), pd.Series(data=memories, name=f)),
        axis=1,
    )

print(tabulate(stats, headers="keys", tablefmt="psql", showindex=False, floatfmt=".6f"))

# Results
# +--------------+--------------+------------+------------+--------------------+--------------------+-----------+---------+
# |   dict_deque |   dict_deque |   frontier |   frontier |   generator_sorted |   generator_sorted |     naive |   naive |
# |--------------+--------------+------------+------------+--------------------+--------------------+-----------+---------|
# |     0.000007 |          nan |   0.000006 |        nan |           0.000004 |                nan |  0.000003 |     nan |
# |     0.000007 |          nan |   0.000006 |        nan |           0.000002 |                nan |  0.000003 |     nan |
# |     0.000007 |          nan |   0.000017 |        nan |           0.000002 |                nan |  0.000002 |     nan |
# |     0.000013 |          nan |   0.000016 |        nan |           0.000005 |                nan |  0.000007 |     nan |
# |     0.000023 |          nan |   0.000018 |        nan |           0.000005 |                nan |  0.000007 |     nan |
# |     8.998981 |          nan |  11.373660 |        nan |           3.219218 |                nan |  2.964407 |     nan |
# |    13.146834 |          nan |  25.976955 |        nan |          11.210449 |                nan | 11.167494 |     nan |
# |     9.018310 |          nan |  11.517480 |        nan |           3.247321 |                nan |  3.079813 |     nan |
# +--------------+--------------+------------+------------+--------------------+--------------------+-----------+---------+

# +---------------------+---------------------+--------------------+--------------------+-----------+---------+
# |   generator_counter |   generator_counter |   generator_sorted |   generator_sorted |     naive |   naive |
# |---------------------+---------------------+--------------------+--------------------+-----------+---------|
# |            0.000010 |                 nan |           0.000003 |                nan |  0.000003 |     nan |
# |            0.000006 |                 nan |           0.000002 |                nan |  0.000002 |     nan |
# |            0.000006 |                 nan |           0.000002 |                nan |  0.000002 |     nan |
# |            0.000009 |                 nan |           0.000009 |                nan |  0.000006 |     nan |
# |            0.000013 |                 nan |           0.000007 |                nan |  0.000007 |     nan |
# |            3.643955 |                 nan |           3.097330 |                nan |  2.980563 |     nan |
# |           12.408472 |                 nan |          11.173836 |                nan | 11.356485 |     nan |
# |            3.629347 |                 nan |           3.217870 |                nan |  3.171647 |     nan |
# +---------------------+---------------------+--------------------+--------------------+-----------+---------+
# +-------------------+-------------------+
# |   generator_heapq |   generator_heapq |
# |-------------------+-------------------|
# |          0.000006 |               nan |
# |          0.000007 |               nan |
# |          0.000005 |               nan |
# |          0.000024 |               nan |
# |          0.000015 |               nan |
# |         22.367247 |               nan |
# |        164.830065 |               nan |
# |         29.500780 |               nan |
# +-------------------+-------------------+
