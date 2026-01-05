from typing import List


class Solution:
    def maxMatrixSum(self, matrix: List[List[int]]) -> int:
        """The matrix can always be reduced to a single minus number.
            If two adjacent numbers have one positive and one negative,
                the negative sign of both is flipped.
            If both are positive, no reason to do anything.
            If both are negative, both become positive.
            So, we can move negative signs through the matrix,
                and we can eliminate negative numbers.
        To maximize sum, we eliminate all negative signs.
        Or we keep one, and use that one the smallest absolute number.
        Accepted. 95%
        """
        total_abs = 0
        min_abs = float("inf")
        odd_negative = False
        for row in matrix:
            for num in row:
                if num < 0:
                    odd_negative = not odd_negative
                    num = -num

                total_abs += num
                if num < min_abs:
                    min_abs = num

        if odd_negative:
            # was added and must be subtracted, so twice.
            return total_abs - 2 * min_abs
        return total_abs


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "1975"
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
        funcs=["maxMatrixSum"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
