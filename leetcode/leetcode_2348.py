from collections import defaultdict
from typing import List


class Solution:
    def zeroFilledSubarray(self, nums: List[int]) -> int:
        """Count number of subsequent zeros n and then apply n*(n+1)/2."""
        return self.one_pass_v2(nums)

    def one_pass_v2(self, nums: List[int]) -> int:
        """Fastest."""
        n = 0  # subsequent zeros
        ans = 0
        for num in nums:
            if num == 0:
                n += 1
            else:
                n = 0
            ans += n
        return ans

    def one_pass(self, nums: List[int]) -> int:
        n = 0  # subsequent zeros
        ans = 0
        for num in nums:
            if num == 0:
                n += 1
            else:
                ans += n * (n + 1) // 2
                n = 0
        ans += n * (n + 1) // 2
        return ans

    def dict_count(self, nums: List[int]) -> int:
        """Store subsequent zero counts in dict before calculating.
        Slower than normal one pass."""
        zeros = defaultdict(int)
        n = 0  # subsequent zeros
        for num in nums:
            if num == 0:
                n += 1
            else:
                zeros[n] += 1
                n = 0

        zeros[n] += 1

        return sum(map(lambda x: x[1] * x[0] * (x[0] + 1) // 2, zeros.items()))

    def array_count(self, nums: List[int]) -> int:
        """Store subsequent zero counts in list before calculating.
        Slower than normal one pass."""
        zeros = [0]  # subsequent zeros
        for num in nums:
            if num == 0:
                zeros[-1] += 1
            else:
                zeros.append(0)

        return sum(map(lambda x: x * (x + 1) // 2, zeros))


# +------------+---------------+--------------+---------------+
# |   one_pass |   array_count |   dict_count |   one_pass_v2 |
# |------------+---------------+--------------+---------------|
# |   0.000003 |      0.000004 |     0.000007 |      0.000001 |
# |   0.000001 |      0.000002 |     0.000003 |      0.000001 |
# |   0.000001 |      0.000001 |     0.000002 |      0.000001 |
# |   0.006356 |      0.009550 |     0.007785 |      0.003766 |
# +------------+---------------+--------------+---------------+


if __name__ == "__main__":
    from timing import timing

    def gen_testcases(n):
        import random

        s = Solution()
        with open("leetcode_2348_data.txt", "a") as fp:
            for _ in range(n):
                x = [random.randint(0, 10) for _ in range(100_000)]
                out = s.one_pass(x)
                string = f"{x}->{out}\n"
                fp.write(string)

    # gen_testcases(1)

    timing(
        solution=Solution(),
        funcs=["one_pass", "array_count", "dict_count", "one_pass_v2"],
        data_file="leetcode_2348_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
