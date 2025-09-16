import math
from typing import List


class Solution:
    def replaceNonCoprimes(self, nums: List[int]) -> List[int]:
        def inner(nums):
            curr = nums[0]
            ans = list()
            for num in nums[1:]:
                if math.gcd(curr, num) > 1:
                    curr = math.lcm(curr, num)
                else:
                    ans.append(curr)
                    curr = num
            ans.append(curr)
            return ans

        while True:
            # normal order
            out = inner(nums)
            # run in reverse order, and then reverse result
            out2 = inner(out[::-1])[::-1]
            if out2 == nums:
                return out2
            nums = out2


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "2197"
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
        funcs=["replaceNonCoprimes"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
