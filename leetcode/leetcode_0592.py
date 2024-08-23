import re
from collections import Counter


def get_prime_factors(n: int) -> list:
    """Also include 0 and 1, to facilitate the combine_factors function and conversion to int ."""
    if n == 0:
        return Counter([0])
    if n < 0:
        factors = [-1]
        n = -n
    else:
        factors = [1]

    factor = 2
    while n > 1:
        while n % factor == 0:
            factors.append(factor)
            n //= factor
        factor = factor + 2 if factor > 2 else factor + 1
    return Counter(factors)


def factors_to_int(factors: Counter) -> int:
    ans = 1
    for factor, count in factors.items():
        ans *= factor**count
    return ans


def combine_factors(
    num1_factors: Counter,
    num2_factors: Counter,
    denom1_factors: Counter,
    denom2_factors: Counter,
) -> int:
    denom_factors = denom1_factors + denom2_factors
    num1_factors += denom2_factors
    num2_factors += denom1_factors
    num = factors_to_int(num1_factors) + factors_to_int(num2_factors)
    num_factors = get_prime_factors(num)
    return num_factors, denom_factors


def reduce_factors(num_factors, denom_factors):
    if 0 in num_factors:
        return Counter([0]), Counter([1])
    overlap = num_factors & denom_factors
    num_factors -= overlap
    denom_factors -= overlap
    return num_factors, denom_factors


class Solution:
    def fractionAddition(self, expression: str) -> str:
        """Just express numerator and denominator as a product of prime integers.
        Then simpifying is easy."""
        fractions = re.findall(r"[+-]?\d+/\d+", expression)

        # initialize with 0/1
        prev_num_factors = Counter([0])
        prev_denom_factors = Counter([1])
        for fraction in fractions:
            # combine two fractions
            numerator, denominator = map(int, fraction.split("/"))
            prev_num_factors, prev_denom_factors = combine_factors(
                prev_num_factors,
                get_prime_factors(numerator),
                prev_denom_factors,
                get_prime_factors(denominator),
            )

            # simplify resulting fraction
            prev_num_factors, prev_denom_factors = reduce_factors(
                prev_num_factors, prev_denom_factors
            )

        return (
            f"{factors_to_int(prev_num_factors)}/{factors_to_int(prev_denom_factors)}"
        )


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["fractionAddition"],
        data_file="leetcode_0592_data.txt",
        data_lines=[0, 1, 2, 3],
    )
