from typing import List


class Solution:
    def isPowerOfTwo(self, n: int) -> bool:
        return self.bit_shift(n)

    def bit_shift(self, n: int) -> bool:
        check = 1
        while check < n:
            check <<= 1
        if check == n:
            return True
        return False

    def in_set(self, n: int) -> bool:
        maxpow = 32
        possibilities = {2**pow for pow in range(maxpow)}
        if n in possibilities or -n in possibilities:
            return True
        return False


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["in_set", "bit_shift"],
        data_file="leetcode_0231_data.txt",
        exclude_data_lines=None,
        repeat=100,
        check_result=True,
    )
