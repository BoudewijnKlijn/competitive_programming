from typing import List


class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        """Single pass."""
        minimum = prices[0]
        ans = 0
        prev = prices[0]
        for price in prices[1:]:
            if price > prev:
                ans = max(ans, price - minimum)
            else:
                minimum = min(minimum, price)
            prev = price
        return ans

    def three_passes(self, prices: List[int]) -> int:
        """One pass from the left to store minimum value.
        One pass from the right to store maximum value.
        One pass to subtract from each other."""
        n = len(prices)

        prefix_min = [0] * n
        prefix_min[0] = prices[0]
        for i, price in enumerate(prices[1 : n - 1], start=1):
            prefix_min[i] = min(prefix_min[i - 1], price)

        prefix_max_right = [0] * n
        prefix_max_right[n - 1] = prices[n - 1]
        for j, price in enumerate(reversed(prices[1 : n - 1]), start=1):
            prefix_max_right[n - j - 1] = max(prefix_max_right[n - j], price)

        ans = 0
        for buy, sell in zip(prefix_min, prefix_max_right[1:]):
            ans = max(ans, sell - buy)
        return ans


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["maxProfit", "three_passes"],
        data_file="leetcode_0121_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
