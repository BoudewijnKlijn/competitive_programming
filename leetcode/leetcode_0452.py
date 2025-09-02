from typing import List


class Solution:
    def findMinArrowShots(self, points: List[List[int]]) -> int:
        """All balloons have to be shot.
        One balloon is the left most balloon, and that too requires an arrow.
        Its best to be greedy and try to shoot as many other balloons with it.
        Shooting more balloons with that arrow, will not make the solution worse.
        Sort balloons left to right.
        Keep adding balloons to the arrow, while left of new is <= than current end.
        Update current end if this end is smaller.
            Cannot go beyond this end, or we would not shoot that balloon.
        """
        points.sort()
        _, current_end = points[0]
        ans = 1
        for start, end in points[1:]:
            if end < current_end:
                current_end = end
            elif start > current_end:
                # new arrow needed
                current_end = end
                ans += 1
        return ans


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "0452"
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
        funcs=["findMinArrowShots"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
