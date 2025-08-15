from math import exp, log


class Solution:
    def myPow(self, x: float, n: int) -> float:
        """Not using the built in power function."""
        if x == 0:
            return 0
        elif x > 0:
            return exp(n * log(x))
        elif n % 2:
            return -exp(n * log(-x))
        else:
            return exp(n * log(-x))
