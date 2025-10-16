from collections import Counter
from typing import List


class Solution:
    def findSmallestInteger(self, nums: List[int], value: int) -> int:
        """The maximum MEX after adding or subtracting value to num in nums, results from
        consecutive array of 0,1,2,n.
        Apply num % value to get all remainders.
        The remainder which occurs fewest will determine the answer.
        """
        return self.faster3(nums, value)

    def faster3(self, nums: List[int], value: int) -> int:
        seen = {remainder: 0 for remainder in range(value)}
        for num in nums:
            remainder = num % value
            seen[remainder] += 1

        ans = len(nums)
        for rem, count in seen.items():
            alternative = rem + value * count
            if alternative < ans:
                ans = alternative
        return ans

    def faster2(self, nums: List[int], value: int) -> int:
        seen = {remainder: 0 for remainder in range(value)}
        for num in nums:
            remainder = num % value
            seen[remainder] += 1

        ans = 0
        remainder = 0
        while seen[remainder] > 0:
            seen[remainder] -= 1
            # faster than calling ans % value repeatedly
            remainder = remainder + 1 if remainder < value - 1 else 0
            ans += 1
        return ans

    def faster(self, nums: List[int], value: int) -> int:
        seen = {rem: 0 for rem in range(value)}
        ans = 0
        idx = 0
        for num in nums:
            rem = num % value
            seen[rem] += 1
            while seen[idx] > 0:
                seen[idx] -= 1
                idx = (
                    idx + 1 if idx < value - 1 else 0
                )  # faster than calling ans % value repeatedly
                ans += 1
        return ans

    def not_so_fast(self, nums: List[int], value: int) -> int:
        remainders = [num % value for num in nums]
        count = Counter(remainders)
        ans = 0
        rem = ans % value
        while rem in count and count[rem] > 0:
            count[rem] -= 1
            ans += 1
            rem = ans % value
        return ans


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "2598"
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
        funcs=["not_so_fast", "faster", "faster2", "faster3"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
