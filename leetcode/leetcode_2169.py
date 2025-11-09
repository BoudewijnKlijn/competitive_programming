class Solution:
    def countOperations(self, num1: int, num2: int) -> int:
        ans = 0
        while num1 and num2:
            if num2 > num1:
                num1, num2 = num2, num1
            div, mod = divmod(num1, num2)
            num1 = mod
            ans += div
        return ans


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "2169"
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
        funcs=["countOperations"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
