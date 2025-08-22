from typing import List


class Solution:

    def __init__(self):
        self.primes = self.get_primes(1000)

    @staticmethod
    def get_primes(n):
        """Get primes up to n."""
        primes = [2, 3]
        for p in range(5, n + 1, 2):
            for prime in primes:
                if p % prime == 0:
                    # not prime
                    break
            else:
                # prime. not divisable by other primes.
                primes.append(p)
        return primes

    def distinctPrimeFactors(self, nums: List[int]) -> int:
        """Product does not change prime factors.
        Just keep set with factors."""

        factors = set()
        for num in nums:
            for prime in self.primes:
                while num % prime == 0:
                    num //= prime
                    factors.add(prime)
                if num == 1:
                    # no more factors to find.
                    break
        return len(factors)


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["distinctPrimeFactors"],
        data_file="leetcode_2521_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
