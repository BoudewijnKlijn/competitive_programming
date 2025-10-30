from typing import List


class Solution:
    def minNumberOperations(self, target: List[int]) -> int:
        """Can also be done in reverse: start from target and subtract to get all zeros.
        A number can also be viewed as an opening/closing bracket.
        We need at least the first number in target as number of operations.
        Can use a count of open brackets, then update count based on new numbers.
            Decrease count (i.e. close bracket) when number is lower.
            Increase count (i.e. open bracket) when number is higher.
            Do nothing if number is the same.
            An opening bracket has to be closed eventually.
            Only increase ans when bracket is opened.
        """
        ans = 0
        prev = 0
        for num in target:
            diff = num - prev
            if diff > 0:
                ans += diff
            prev = num
        return ans


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "1526"
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
        funcs=["minNumberOperations"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
