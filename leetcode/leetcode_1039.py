from functools import cache
from math import prod
from typing import List


class Solution:
    def minScoreTriangulation(self, values: List[int]) -> int:
        # return self.bruteforce(values)
        return self.greedy(values)

    def greedy(self, values: List[int]) -> int:
        """Remove node with max value --> does not work (see test case: 4,3,1,3).
        Combine three nodes with smallest values --> does not work (see test case: 4,3,1,3).
        """

        def inner(values):
            n = len(values)
            if n < 3:
                return 0
            elif n == 3:
                return prod(values)

            sorted_values = sorted(enumerate(values), key=lambda x: x[1])
            smallest_three_idxs = sorted([x for x, _ in sorted_values[:3]])
            ans = prod([v for _, v in sorted_values[:3]])
            ans += inner(values[smallest_three_idxs[0] : smallest_three_idxs[1] + 1])
            ans += inner(values[smallest_three_idxs[1] : smallest_three_idxs[2] + 1])
            ans += inner(
                values[smallest_three_idxs[2] :] + values[: smallest_three_idxs[0] + 1]
            )
            return ans

        return inner(values)

    def recursion(self, values: List[int]) -> int:
        """Can be split into subproblems.
        Every time we can 'break off' one node.
            We add the sum product and feed the remaining nodes into algorithm again.

        Time Limit Exceeded
        76 / 94 testcases passed
        """

        @cache
        def inner(values):
            n = len(values)
            if n == 3:
                return prod(values)

            best = None
            for remove_idx in range(n):
                remaining_values = values[:remove_idx] + values[remove_idx + 1 :]
                ans = (
                    values[remove_idx - 1]
                    * values[remove_idx]
                    * values[(remove_idx + 1) % n]
                ) + inner(remaining_values)
                if best is None or ans < best:
                    best = ans
            return best

        values = tuple(values)
        return inner(values)


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "1039"
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
        funcs=[
            "recursion",
            # "greedy"
        ],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
