import bisect
from typing import List


class Solution:
    def successfulPairs(
        self, spells: List[int], potions: List[int], success: int
    ) -> List[int]:
        return self.two_pointers(spells, potions, success)

    def two_pointers(
        self, spells: List[int], potions: List[int], success: int
    ) -> List[int]:
        """Faster than binary search.
        199ms Beats 84.54%
        """
        n = len(spells)
        m = len(potions)
        potions.sort(reverse=True)
        frac = [-(-success // potion) for potion in potions] + [success + 1]

        # two pointers
        ans = [None] * n
        sorted_spells = sorted(enumerate(spells), key=lambda x: x[1])
        lo = 0
        for idx, spell in sorted_spells:
            while lo < m and spell >= frac[lo]:
                lo += 1
            ans[idx] = lo
        return ans

    def binary_search(
        self, spells: List[int], potions: List[int], success: int
    ) -> List[int]:
        """275ms Beats 77.71%"""
        n = len(spells)
        potions.sort(reverse=True)
        frac = [-(-success // potion) for potion in potions]

        # binary search
        ans = [None] * n
        seen = set()
        sorted_spells = sorted(enumerate(spells), key=lambda x: x[1])
        lo = 0
        for idx, spell in sorted_spells:
            if spell not in seen:
                lo = bisect.bisect_right(frac, spell, lo=lo)
                seen.add(spell)
            ans[idx] = lo
        return ans


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "2300"
    data_file = os.path.join(os.path.dirname(__file__), f"leetcode_{PROBLEM}_data.txt")

    # # generate testcases
    # import sys

    # sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    # from generic.helper import InputInteger, InputList, generate_testcases

    # arr1 = InputList(n_min_max=(2, 100_000), val_min_max=(0, 10_000))
    # int1 = InputInteger(val_min_max=(0, 10_000))
    # vars = generate_testcases(structure=(arr1,), n=1, data_file=data_file, solver=None)

    timing(
        solution=Solution(),
        funcs=["binary_search", "two_pointers"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
