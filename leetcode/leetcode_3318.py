import heapq
from collections import Counter
from math import prod
from typing import List


class Solution:
    def findXSum(self, nums: List[int], k: int, x: int) -> List[int]:
        return self.reuse(nums, k, x)

    def reuse(self, nums: List[int], k: int, x: int) -> List[int]:
        """Create counter objects once and reuse it. One items enters window, another is removed."""

        def get_x_sum(count, x):
            # sorted_count = sorted(count.items(), key=lambda x: (-x[1], -x[0]))
            # return sum(map(prod, sorted_count[:x]))

            # using heapq can more efficient for large arrays and small x.
            top = heapq.nlargest(x, [(c[1], c[0]) for c in count.items()])
            return sum(map(prod, top))

        ans = list()
        n = len(nums)
        for i in range(n - k + 1):
            if i == 0:
                count = Counter(nums[i : i + k])
            else:
                count[nums[i - 1]] -= 1
                count[nums[i + k - 1]] += 1

            ans.append(get_x_sum(count, x))
        return ans

    def naive(self, nums: List[int], k: int, x: int) -> List[int]:
        """Very small constraints. Implement function and apply several times."""

        def get_x_sum(arr, x):
            count = Counter(arr)
            sorted_count = sorted(count.items(), key=lambda x: (-x[1], -x[0]))
            return sum(map(prod, sorted_count[:x]))

        ans = list()
        n = len(nums)
        for i in range(n - k + 1):
            ans.append(get_x_sum(nums[i : i + k], x))

        return ans


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "3318"
    data_file = os.path.join(os.path.dirname(__file__), f"leetcode_{PROBLEM}_data.txt")

    # # generate testcases
    # import sys

    # sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    # from generic.helper import InputInteger, InputList, generate_testcases

    # arr1 = InputList(n_min_max=(2, 100_000), val_min_max=(0, 10_000))
    # int1 = InputInteger(val_min_max=(0, 10_000))
    # vars = generate_testcases(structure=(arr1,), n=1, data_file=data_file, solver=None)

    timing(
        solution=Solution(),
        funcs=["naive", "reuse"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
