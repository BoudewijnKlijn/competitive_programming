from collections import deque


class Solution:
    def makeTheIntegerZero(self, num1: int, num2: int) -> int:
        return self.faster(num1, num2)

    def faster(self, num1: int, num2: int) -> int:
        """If we can make num1 in n operations, then we have added n*num2 + some number n of combinations
            of powers of 2. e.g. 1+2+2 is 3 combinations, and we also added 3*num2.
        Let's start from the assumption that we can do it in n operations.
            Then we must be able to create d = num1-n*num2 from n combinations of powers of 2.
            If d has n bits, then that is the solution.
            The same bit can also be used again...
                The 2nd bit can also be expressed as 2x the first bit.
                The 3rd bit can also be expressed as 2x the second bit, or 4x the first bit, etc.
                So, if we have more bits than operations, we can accept it as solution.
                Unless, we __only__ have the first bit. E.g. if n=2 and we have to create d=1, then
                    that is not possible. The smallest number we can make is n times the first bit,
                    so n*1=n. Hence, d must be larger than or equal to n.
        """
        n = 1
        d = num1 - num2
        while d >= n:
            bits = bin(d)
            n_one_bits = bits[2:].count("1")
            if n_one_bits <= n:
                return n
            n += 1
            d -= num2
        return -1

    def too_slow(self, num1: int, num2: int) -> int:
        """We subtract 2**i + num2 from num1, with i in range 0-60.
        Can also do it in reverse. Start from zero and see which numbers we can make.
        Slow because many numbers are created which are not useful.
        """
        seen = set()
        stack = deque([(0, 0)])
        always_increasing = num2 > -1
        add_list = [2**i + num2 for i in range(60)]
        while stack:
            num, n = stack.popleft()
            for add in add_list:
                new = num + add
                if new > 1e9 or (always_increasing and new > num1):
                    # out of bounds
                    # number is larger and will only become larger, so can never become num1
                    break
                if new in seen:
                    # already tried
                    continue
                if new == num1:
                    return n + 1
                seen.add(new)
                stack.append((new, n + 1))
        return -1


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "2749"
    data_file = os.path.join(os.path.dirname(__file__), f"leetcode_{PROBLEM}_data.txt")

    # generate testcases
    import sys

    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from generic.helper import InputInteger, generate_testcases

    int1 = InputInteger(val_min_max=(1, 1000))
    int2 = InputInteger(val_min_max=(-1000, 1000))
    vars = generate_testcases(
        structure=(int1, int2), n=10, data_file=data_file, solver=Solution().too_slow
    )

    timing(
        solution=Solution(),
        funcs=[
            # "makeTheIntegerZero",
            # "too_slow",
            "faster",
        ],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
