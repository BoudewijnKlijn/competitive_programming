from typing import List


class Solution:
    def getNoZeroIntegers(self, n: int) -> List[int]:
        def check_no_zero(num):
            if num < 1:
                return False

            while num > 0:
                num, mod = divmod(num, 10)
                if mod == 0:
                    return False
            return True

        a = 1
        b = n - 1
        while True:
            if check_no_zero(a) and check_no_zero(b):
                return [a, b]
            a += 1
            b -= 1


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "1317"
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
        funcs=["getNoZeroIntegers"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
