from typing import List


class Solution:
    # precompute all powers of four within bounds
    powers_of_four = {4**pow for pow in range(16)}

    def isPowerOfFour(self, n: int) -> bool:
        """Same as leetcode 326."""
        return self.times4(n)

    def precompute(self, n):
        return n in self.powers_of_four

    def times4(self, n):
        check = 1
        while check < n:
            check *= 4
        if check == n:
            return True
        return False

    def bitshift2(self, n):
        check = 1
        while check < n:
            check <<= 2
        if check == n:
            return True
        return False


if __name__ == "__main__":
    from timing import timing

    def gen_testcases(n):
        import random

        s = Solution()
        with open("leetcode_0342_data.txt", "a") as fp:
            for _ in range(n):
                x = random.randint(0, 2147483647)
                out = s.times4(x)
                string = f"{x}->{out}\n"
                fp.write(string)

            x = 1
            for _ in range(10):
                x *= 4
                out = s.times4(x)
                string = f"{x}->{out}\n"
                fp.write(string)

    # gen_testcases(10)

    timing(
        solution=Solution(),
        funcs=[
            "times4",
            "bitshift2",
            "precompute",
        ],
        data_file="leetcode_0342_data.txt",
        exclude_data_lines=None,
        repeat=100,
        check_result=True,
    )
