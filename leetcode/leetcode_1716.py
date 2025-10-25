class Solution:
    ans = [0]
    monday = 1
    i = 0

    while len(ans) <= 1000:
        if i == 0:
            extra = monday
            monday += 1
        else:
            extra += 1
        ans.append(ans[-1] + extra)
        i = i + 1 if i < 6 else 0

    def totalMoney(self, n: int) -> int:
        """Precalculate all answers."""
        return self.ans[n]


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "1716"
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
        funcs=["totalMoney"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
