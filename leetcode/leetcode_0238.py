from collections import Counter
from itertools import chain
from math import prod
from typing import List


class Solution:

    def __init__(self):
        self.primes = self.get_primes(30)

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

    def productExceptSelf(self, nums: List[int]) -> List[int]:
        return self.factor_decomposition(nums)

    def factor_decomposition(self, nums: List[int]) -> List[int]:
        """Division is not allowed. O(n) solution required.
        Get prime factors of all numbers. Store in list and store count of all in dict.
        Subtract count from dict and take product of factors to the right power.
        """

        def get_factors(num):
            if num == 0:
                return [0]
            elif num < 0:
                factors = [-1]
                num *= -1
            else:
                factors = [1]

            for prime in self.primes:
                while num > 1 and num % prime == 0:
                    num //= prime
                    factors.append(prime)
                if num == 1:
                    return factors

        count_nums = Counter(nums)
        factors_for_num = {num: get_factors(num) for num in count_nums}

        def get_ans(num):
            if num in memo:
                return memo[num]
            remaining_factors = count_all_factors - Counter(factors_for_num[num])
            memo[num] = prod(k**v for k, v in remaining_factors.items())
            return memo[num]

        # combine the values of the counter of factors AND the counter of nums
        count_all_factors = Counter(
            chain.from_iterable(v * count_nums[k] for k, v in factors_for_num.items())
        )
        memo = {}
        return [get_ans(num) for num in nums]


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["productExceptSelf"],
        data_file="leetcode_0238_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
