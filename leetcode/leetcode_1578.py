from typing import List


class Solution:
    def minCost(self, colors: str, neededTime: List[int]) -> int:
        """Of a streak of the same colors, add all neededTimes except for the largest.
        Remember the last/largest time. Determine if new time is smaller. Add the smallest time.
        38ms Beats 98.72%
        """
        n = len(colors)
        prev = None
        largest_time = None
        ans = 0
        for i in range(n):
            if colors[i] == prev:
                if neededTime[i] > largest_time:
                    ans += largest_time
                    largest_time = neededTime[i]
                else:
                    ans += neededTime[i]
            else:
                prev = colors[i]
                largest_time = neededTime[i]
        return ans


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "1578"
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
        funcs=["minCost"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
