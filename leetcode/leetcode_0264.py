import heapq
from itertools import count


class Solution:
    def nthUglyNumber(self, n: int) -> int:
        """Instead of verifying all numbers, I make generators that spit out multiples of 2, 3, 5.
        Thats probably quicker, and a lot simpler.
        I avoid trying all multilples. Only ugly numbers as multiples to be sure the result is ugly as well.
        """
        if n == 1:
            return 1

        ugly_numbers_set = {1}
        ugly_numbers = [1]

        def multiples(base):
            for idx in count():
                yield ugly_numbers[idx] * base

        for x in heapq.merge(multiples(2), multiples(3), multiples(5)):
            if x in ugly_numbers_set:
                continue

            ugly_numbers_set.add(x)
            ugly_numbers.append(x)
            if len(ugly_numbers) == n:
                return x


# s = Solution()
# print(s.nthUglyNumber(1690))
