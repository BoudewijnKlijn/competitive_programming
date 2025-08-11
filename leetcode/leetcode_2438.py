from math import prod
from typing import List


class Solution:
    def productQueries(self, n: int, queries: List[List[int]]) -> List[int]:
        bits = bin(n)[2:]
        powers = list()
        power_of_2 = 1
        for bit in map(int, bits[::-1]):
            if bit:
                powers.append(power_of_2)
            power_of_2 <<= 1

        ans = list()
        for left, right in queries:
            ans.append(prod(powers[left : right + 1]) % (1_000_000_000 + 7))

        return ans


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["productQueries"],
        data_file="leetcode_2438_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
