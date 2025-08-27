

class Solution:
    # precompute all powers of three within bounds
    powers_of_three = {3**pow for pow in range(20)}

    def isPowerOfThree(self, n: int) -> bool:
        return self.times3(n)

    def prime_factor(self, n):
        """Someone else's leetcode idea.
        In every 3**x, the only prime factor is 3.
        If we take a large power like 3**19, then again its only prime factors are 3
            and divisors are 3 or powers of three.
        If 3**19 mod n == 0, then n must be a power of 3, since only powers of three are divisors,
            hence result in no remainder.
        3**19 = 1162261467"""
        return n > 0 and 1162261467 % n == 0

    def precompute(self, n):
        return n in self.powers_of_three

    def times3(self, n):
        check = 1
        while check < n:
            check *= 3
        if check == n:
            return True
        return False

    def in_set(self, n: int) -> bool:
        if n <= 0:
            return False

        maxpow = 19 + 1
        possibilities = {3**pow for pow in range(maxpow)}
        if n in possibilities:
            return True
        return False


if __name__ == "__main__":
    from timing import timing

    def gen_testcases(n):
        import random

        s = Solution()
        with open("leetcode_0326_data.txt", "a") as fp:
            for _ in range(n):
                x = random.randint(0, 2147483647)
                out = s.times3(x)
                string = f"{x}->{out}\n"
                fp.write(string)

            x = 1
            for _ in range(20):
                x *= 3
                out = s.times3(x)
                string = f"{x}->{out}\n"
                fp.write(string)

    # gen_testcases(10)

    timing(
        solution=Solution(),
        funcs=[
            "in_set",
            "times3",
            "prime_factor",
            "precompute",
        ],
        data_file="leetcode_0326_data.txt",
        exclude_data_lines=None,
        repeat=100,
        check_result=True,
    )
