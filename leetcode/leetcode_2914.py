from itertools import batched


class Solution:
    def minChanges(self, s: str) -> int:
        """There is no cost to making many partitions.
        Every partition needs to have even length.
        We can just consider partitions of length 2, all the time.
        If both zero, or both one, we don't need to do anything.
        If not equal, it requires one change: ans++.
        """
        return self.with_zip(s)

    def with_index(self, s: str) -> int:
        i = 0
        ans = 0
        while i < len(s):
            if s[i] != s[i + 1]:
                ans += 1
            i += 2
        return ans

    def with_builtin_batch(self, s: str) -> int:
        """Python 3.12+"""
        ans = 0
        for char1, char2 in batched(s, 2):
            if char1 != char2:
                ans += 1
        return ans

    def with_zip(self, s: str) -> int:
        ans = 0
        for char1, char2 in zip(s[::2], s[1::2]):
            if char1 != char2:
                ans += 1
        return ans

    def simple(self, s: str) -> int:
        n = len(s)
        ans = 0
        for i in range(0, n, 2):
            if s[i] != s[i + 1]:
                ans += 1
        return ans


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["simple", "with_zip", "with_builtin_batch", "with_index"],
        data_file="leetcode_2914_data.txt",
        exclude_data_lines=None,
        check_result=True,
        repeat=100,
    )

# +----------+------------+----------------------+--------------+
# |   simple |   with_zip |   with_builtin_batch |   with_index |
# |----------+------------+----------------------+--------------|
# | 0.000029 |   0.000041 |             0.000029 |     0.000024 |
# | 0.000023 |   0.000036 |             0.000024 |     0.000018 |
# | 0.000026 |   0.000037 |             0.000026 |     0.000022 |
# | 0.035989 |   0.019790 |             0.024378 |     0.048506 |
# +----------+------------+----------------------+--------------+
