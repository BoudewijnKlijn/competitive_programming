from typing import List


class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        """Buy stock for first price.
        If next day is lower, then act as if we don't have stock and buy that.
            Update buy price to lower value.
        Repeat, until next day is higher, then sell the stock. Update profit.
        If next day is higher, act as if not sold and sell for higher price.
            Increase profit.
        If next day is lower, buy stock and start over."""
        minimum = prices[0]
        profit = 0
        for price in prices[1:]:
            if price > minimum:
                profit += price - minimum
            minimum = price
        return profit


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["maxProfit"],
        data_file="leetcode_0122_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
