import heapq
import timeit
from collections import Counter, deque
from functools import partial
from itertools import combinations, repeat
from typing import List


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
        return self.binary_search(nums, k)

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
        """Memory limit exceeded. Slightly slower than naive.
        18/19 passed."""
        nums.sort()
        return sorted(b - a for a, b in combinations(nums, 2))[k - 1]

    @staticmethod
    def generator_counter(nums, k):
        """Should have lower memory because diffs stored in Counter.
        Slightly slower than naive.
        18/19 passed. Time limit exceeded.
        !! Apparently this is a solution from the editorial, but it has time limit exceeded when using Python.
        """
        nums.sort()
        c = Counter(b - a for a, b in combinations(nums, 2))
        for diff, count in sorted(c.items()):
            if count >= k:
                return diff
            k -= count

    @staticmethod
    def binary_search(nums, k):
        """Adjust distance with binary search.
        For each distance determine how many pairs have that distance or less.
        If number of pairs is less than k, then we increase the distance.
        If number of pairs is more than k, then we decrease the distance.
        19/19 passed."""
        nums.sort()
        max_num = nums[-1]
        counts = Counter(nums)
        # sort dict, such that we can loop over keys instead of nums
        counts = dict(sorted(counts.items()))
        # cumulative number of values less than or equal to value
        lte_counts = [0] * (max_num + 1)
        total = 0
        for value in range(max_num + 1):
            total += counts.get(value, 0)
            lte_counts[value] = total

        # assuming some distance, how many pairs have that distance or less
        def count_within_distance(distance):
            """Calculate number of pairs with distance or less."""
            combinations = 0
            for num, count in counts.items():
                larger_values_within_distance = (
                    lte_counts[min(max_num, num + distance)] - lte_counts[num]
                )
                combinations_with_self = count * (count - 1) // 2
                combinations += (
                    combinations_with_self + larger_values_within_distance * count
                )
            return combinations

        # adjust distance with binary search
        left = 0
        right = max_num - nums[0]
        while left < right:
            mid = (left + right) // 2
            if count_within_distance(mid) < k:
                left = mid + 1
            else:
                right = mid
        return left

    @staticmethod
    def frontier_heapq(nums, k):
        """Only stores differences of numbers that are at frontier: uses less memory.
        Using insert order as secondary key makes it slower.
        17/19 passed. Time limit exceeded."""
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
    def heapq_merge(nums, k):
        """Similar idea as frontier, but using a builtin method.
        Similar speed as frontier.
        16/19 passed. Time limit exceeded."""

        def row(r):
            for c in range(r + 1, len(nums)):
                yield nums[c] - nums[r]

        nums.sort()
        diff = heapq.merge(*(row(start) for start in range(len(nums) - 1)))
        for _ in range(k - 1):
            next(diff)
        return next(diff)

    # @staticmethod
    # def generator_heapq(nums, k):
    #     """Slowwww"""
    #     nums.sort()
    #     return heapq.nsmallest(k, (b - a for a, b in combinations(nums, 2)))[-1]

    @staticmethod
    def frontier_dict(nums, k):
        """Use dict with deques instead of heapq.
        Still using frontier, so low memory usage.
        Faster than heapq, but not fast enough.
        17/19 passed. Time limit exceeded."""
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
            if len(diffs[minimum]) == 0:
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

solution = Solution()
stats = pd.DataFrame()
params = [
    ([1, 3, 1], 1, 0),
    ([1, 1, 1], 2, 0),
    ([1, 6, 1], 3, 5),
    ([9, 10, 7, 10, 6, 1, 5, 4, 9, 8], 18, 2),
    ([38, 33, 57, 65, 13, 2, 86, 75, 4, 56], 26, 36),
    *[
        (file_to_list_int(file), k, ans)
        for k, (file, ans) in zip(
            repeat(25_000_000),
            [
                ("leetcode_0719_nums0.txt", 1),
                ("leetcode_0719_nums1.txt", 292051),
                ("leetcode_0719_nums2.txt", 3),
            ],
        )
    ],
]
funcs = [func for func in dir(Solution) if not func.startswith("__")]
for func in funcs:
    print(f"\nRunning {func}")
    if func == "smallestDistancePair":
        continue

    runtimes = []
    for i, (nums, k, a) in enumerate(params):
        print(f"{i}", end=", ")
        method = getattr(solution, func)
        test_func = partial(method, nums, k)
        runtime = timeit.timeit(test_func, globals=globals(), number=1)
        runtimes.append(runtime)
        if runtime < 1e-3:
            ans = test_func()
            assert ans == a, f"{func}: {ans} != {a}"

    stats = pd.concat((stats, pd.Series(data=runtimes, name=func)), axis=1)

print(tabulate(stats, headers="keys", tablefmt="psql", showindex=False, floatfmt=".6f"))

# Results
# +-----------------+-----------------+------------------+---------------------+--------------------+---------------+-----------+
# |   binary_search |   frontier_dict |   frontier_heapq |   generator_counter |   generator_sorted |   heapq_merge |     naive |
# |-----------------+-----------------+------------------+---------------------+--------------------+---------------+-----------|
# |        0.000053 |        0.000017 |         0.000010 |            0.000050 |           0.000006 |      0.000027 |  0.000006 |
# |        0.000008 |        0.000011 |         0.000008 |            0.000006 |           0.000003 |      0.000013 |  0.000003 |
# |        0.000011 |        0.000009 |         0.000007 |            0.000006 |           0.000003 |      0.000012 |  0.000002 |
# |        0.000015 |        0.000017 |         0.000018 |            0.000010 |           0.000007 |      0.000027 |  0.000008 |
# |        0.000028 |        0.000031 |         0.000018 |            0.000016 |           0.000007 |      0.000025 |  0.000008 |
# |        0.000655 |        9.547940 |        11.592176 |            3.821516 |           3.318446 |     17.119955 |  2.893914 |
# |        0.168112 |       13.774853 |        26.867289 |           15.396069 |          12.049748 |     23.595636 | 12.281599 |
# |        0.000840 |        9.897670 |        11.681771 |            3.719117 |           3.341385 |     16.820555 |  3.243417 |
# +-----------------+-----------------+------------------+---------------------+--------------------+---------------+-----------+
# +-------------------+
# |   generator_heapq |
# |-------------------+
# |          0.000006 |
# |          0.000007 |
# |          0.000005 |
# |          0.000024 |
# |          0.000015 |
# |         22.367247 |
# |        164.830065 |
# |         29.500780 |
# +-------------------+
