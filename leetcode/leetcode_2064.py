from collections import Counter
from typing import List


class Solution:
    def minimizedMaximum(self, n: int, quantities: List[int]) -> int:
        """Use binary search.
        start with minimum=1, maximum=max(quantities). Then search.
        If more stores needed than available, increase the quantity per store."""
        left = 1
        quantities_counts = Counter(quantities)
        right = max(quantities_counts.keys())

        def calc_stores_needed(quantities_counts, quantity_per_store):
            if quantity_per_store == 0:
                return 1e6
            stores_needed = 0
            for quantity, count in quantities_counts.items():
                stores, mod = divmod(quantity, quantity_per_store)
                stores_needed += stores * count
                if mod:
                    stores_needed += count
            return stores_needed

        # binary search
        while left < right:
            mid = (left + right) // 2  # quantity per store
            stores_needed = calc_stores_needed(quantities_counts, mid)
            if stores_needed > n:
                left = mid + 1
            else:
                right = mid
        return left


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["minimizedMaximum"],
        data_file="leetcode_2064_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
