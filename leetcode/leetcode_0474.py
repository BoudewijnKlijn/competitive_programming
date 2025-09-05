from collections import Counter
from functools import cache
from typing import List, Tuple


class Solution:
    def findMaxForm(self, strs: List[str], m: int, n: int) -> int:
        return self.two_dim_dp(strs, m, n)

    def two_dim_dp(self, strs: List[str], m: int, n: int) -> int:
        strs = [(string.count("0"), string.count("1")) for string in strs]
        counts = Counter(strs)
        dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
        seen = set([(0, 0)])
        for (zero_count, one_count), v in counts.items():
            tmp_seen = seen.copy()
            dp_prev = [row[:] for row in dp]
            for zero_seen, one_seen in seen:
                for i in range(1, v + 1):
                    zero = zero_seen + zero_count * i
                    one = one_seen + one_count * i
                    if zero > m or one > n:
                        break
                    dp[zero][one] = max(
                        dp_prev[zero_seen][one_seen] + i, dp_prev[zero][one]
                    )
                    new = zero, one
                    tmp_seen.add(new)
            seen = tmp_seen

        return max(max(row) for row in dp)

    def too_much_memory(self, strs: List[str], m: int, n: int) -> int:
        """Memory Limit Exceeded"""

        @cache
        def inner(strs: Tuple[str], m: int, n: int) -> int:
            if not strs:
                return 0

            zero_count = strs[0].count("0")
            one_count = strs[0].count("1")
            if m - zero_count >= 0 and n - one_count >= 0:
                return max(
                    1 + inner(strs[1:], m - zero_count, n - one_count),
                    inner(strs[1:], m, n),
                )
            return inner(strs[1:], m, n)

        strs = tuple(strs)
        return inner(strs, m, n)


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "0474"
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
        funcs=["findMaxForm", "too_much_memory", "two_dim_dp"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
