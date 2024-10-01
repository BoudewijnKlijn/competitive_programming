from collections import Counter
from typing import List


class Solution:
    def canArrange(self, arr: List[int], k: int) -> bool:
        # Not possible of sum is not divisible by k.
        if sum(arr) % k != 0:
            return False

        # Compute modulo and use Counter for potentially parallel processing.
        arr_modk = [n % k for n in arr]
        counts = Counter(arr_modk)
        while counts:
            key, value = counts.popitem()
            # If key is 0 or k/2 then it should be compared with itself, so has to be even.
            if 2 * key in [0, k] and value % 2 == 0:
                continue
            # Get counterpart, and remove that as well.
            elif counts.get(k - key) == value:
                counts.pop(k - key)
                continue
            # Otherwise, not possible.
            return False
        return True


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["canArrange"],
        data_file="leetcode_1497_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
