from typing import List


class Solution:
    def minOperations(self, queries: List[List[int]]) -> int:
        """The values in the query are between 1 and 1e9.
        For 1-3 (4**0 and 4**1-1), 1 division is needed.
        For 4-15 (4**1 and 4**2-1), 2 divisions are needed.
        For 16-63 (4**2 and 4**3-1), 3 divisions are needed.
        Etc.
        Determine total floor divisions needed.
        We can do two floor divisions per turn. Unless left == right.
        Then sum over all queries."""

        # precompute powers of 4
        powers = {power: 4**power for power in range(0, 16)}

        ans = 0
        for left, right in queries:
            extra = 0
            if left == right:
                # if only one number than can only do one division per turn
                while left > 0:
                    left //= 4
                    extra += 1
                ans += extra
                continue

            for pow in range(1, 16):
                bot = powers[pow - 1]
                top = powers[pow] - 1
                if top < left:
                    continue
                elif bot > right:
                    break
                else:
                    # determine overlap: how many numbers between bot/left and top/right
                    n = min(top, right) - max(bot, left) + 1
                    extra += n * pow

            div, mod = divmod(extra, 2)
            ans += div + 1 if mod else div
        return ans


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "3495"
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
        funcs=["minOperations"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
