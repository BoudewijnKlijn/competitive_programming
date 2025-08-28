from typing import List


class Solution:
    def summaryRanges(self, nums: List[int]) -> List[str]:
        if not nums:
            return []

        ans = list()
        start = None
        prev = None
        for num in nums:
            if start is None:
                start = num
            if prev is None:
                pass
            else:
                diff = num - prev
                if diff == 1:
                    pass
                else:
                    if start == prev:
                        ans.append(f"{start}")
                    else:
                        ans.append(f"{start}->{prev}")
                    start = num
            prev = num

        if start == prev:
            ans.append(f"{start}")
        else:
            ans.append(f"{start}->{prev}")
        return ans


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "0228"
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
        funcs=["summaryRanges"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
