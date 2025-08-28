from typing import List


class Solution:
    def containsNearbyDuplicate(self, nums: List[int], k: int) -> bool:
        last_seen = dict()
        for i in range(len(nums)):
            num = nums[i]
            if num in last_seen and i - last_seen[num] <= k:
                return True
            last_seen[num] = i
        return False


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "0219"
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
        funcs=["containsNearbyDuplicate"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
