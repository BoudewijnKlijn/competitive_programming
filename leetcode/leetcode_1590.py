from itertools import accumulate
from typing import List


class Solution:
    def minSubarray(self, nums: List[int], p: int) -> int:
        return self.two_prefix_sums(nums, p)

    def two_prefix_sums(self, nums: List[int], p: int) -> int:
        """Calculate cumulative sum from the front and from the back.
        For each sum from the front, determine remainder.
        Check if p - remainder is present in the sum from the back.
        If multiple then determine the best."""
        remainder_list = [0] + list(x % p for x in accumulate(nums))
        if remainder_list[-1] == 0:
            return 0

        N = len(nums)

        remainder_list_back = [0] + list(x % p for x in accumulate(nums[::-1]))
        remainders_back = dict()
        for j, prefix in enumerate(remainder_list_back):
            remainder_sum = prefix % p
            if remainder_sum in remainders_back:
                remainders_back[remainder_sum].append(j)
            else:
                remainders_back[remainder_sum] = [j]

        ans = N
        for i, remainder in enumerate(remainder_list):
            if (p - remainder) % p in remainders_back:
                for j in remainders_back[(p - remainder) % p]:
                    if i + j < N:
                        ans = min(ans, N - (i + j))
        if ans == N:
            return -1
        return ans

    def naive_with_pruning(self, nums: List[int], p: int) -> int:
        """Try all subarray lengths, but prune along the way
        pruning: keep shortest length of duplicate subarray sums"""
        remainder = sum(nums) % p
        if remainder == 0:
            return 0

        N = len(nums)
        options = {0: 0}
        ans = N
        for num in nums:
            new_options = {0: 0}
            for total, length in options.items():
                new_total = (total + num) % p
                if new_total in new_options:
                    # keep the shortest subarray length
                    new_options[new_total] = min(new_options[new_total], length + 1)
                else:
                    new_options[new_total] = length + 1
            options = new_options
            if remainder in options:
                ans = min(ans, options[remainder])
        if ans == N:
            return -1
        return ans

    def naive(self, nums: List[int], p: int) -> int:
        """Try all subarray lengths."""
        prefix_sum = [0] + list(accumulate(nums))
        remainder = prefix_sum[-1] % p
        if remainder == 0:
            return 0

        for length in range(1, len(nums)):
            for sum1, sum2 in zip(prefix_sum[:-length], prefix_sum[length:]):
                if (sum2 - sum1) % p == remainder:
                    return length
        return -1


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["naive", "naive_with_pruning", "two_prefix_sums"],
        data_file="leetcode_1590_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
