from collections import Counter, deque
from functools import cache


class Solution:
    # build array with solutions first
    # can be used multiple times
    DP = {i: 1 for i in range(-25, 1)}
    for i in range(1, 100001):
        DP[i] = DP[i - 26] + DP[i - 25]

    def lengthAfterTransformations(self, s: str, t: int) -> int:
        """There are only 26 possible characters in s.
        Length of each character after t transformatings can be computed individually.
        f('a', t) == f('b', t-1).
        Length only increases by one after character 'z' becomes 'ab'."""
        return self.everything_as_z(s, t)

    def everything_as_z(self, s: str, t: int) -> int:
        """Write everything as z. a -> (z, t-25), b -> (z, t-24)
        Then at most ~1e5 possibilities to check. Build up from small values of t.
        Lastly use counter, dict lookup, and multiply.

        Accepted
        824 / 824 testcases passed
        47ms Beats 99.76%"""

        # # build DP first. (done once outside function)
        # DP = {i: 1 for i in range(-25, 1)}
        # for i in range(1, 100001):
        #     DP[i] = DP[i - 26] + DP[i - 25]
        counts = Counter(s)
        ans = 0
        for char, v in counts.items():
            ans += v * self.DP[t - (ord("z") - ord(char))]
        return ans % (10**9 + 7)

    def recursion(self, s: str, t: int) -> int:
        """and memoization
        Memory Limit Exceeded
        814 / 824 testcases passed"""

        @cache
        def inner(steps_to_z, t):
            if t > steps_to_z:
                return inner(25, t - steps_to_z - 1) + inner(24, t - steps_to_z - 1)
            return 1

        ans = 0
        for char in s:
            ans += inner(ord("z") - ord(char), t)

        return ans % (10**9 + 7)

    def naive(self, s: str, t: int) -> int:
        """Time Limit Exceeded
        502 / 824 testcases passed"""
        q = deque()
        for char in s:
            q.append((ord("z") - ord(char), t))

        ans = 0
        while q:
            steps_to_z, t = q.popleft()
            if t > steps_to_z:
                q.append((25, t - steps_to_z - 1))
                q.append((24, t - steps_to_z - 1))
            else:
                ans += 1
        return ans % (10**9 + 7)


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=[
            # "naive",
            # "recursion",
            "everything_as_z",
            "lengthAfterTransformations",
        ],
        data_file="leetcode_3335_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
