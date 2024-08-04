from typing import List


class Solution:
    def rangeSum(self, nums: List[int], n: int, left: int, right: int) -> int:

        def simple(nums, n, left, right):
            """Slowest and most memory."""
            sums = []
            for length in range(1, n + 1):
                for start in range(n + 1 - length):
                    sums.append(sum(nums[start : start + length]))
            return int(sum(sorted(sums)[left - 1 : right]) % (1e9 + 7))

        def faster(nums, n, left, right):
            """Faster, but same memory usage."""
            sums = []
            for i in range(n):
                s = 0
                for n in nums[i:]:
                    s += n
                    sums.append(s)
            return int(sum(sorted(sums)[left - 1 : right]) % (1e9 + 7))

        def faster_and_smaller_storage(nums, n, left, right):
            """Same as faster, but less memory.
            Stores sums and counts in a dict."""
            sums = {}
            for i in range(n):
                s = 0
                for n in nums[i:]:
                    s += n
                    sums[s] = sums.get(s, 0) + 1

            # loop over the sums and counts
            # add after items are skipped
            # stop adding when right is reached
            total = 0
            skip = left - 1
            remaining = right - skip
            for k, v in sorted(sums.items()):
                if skip > v:
                    skip -= v
                    continue
                elif skip > 0:
                    v -= skip
                    skip = 0

                if remaining > v:
                    remaining -= v
                    total += v * k
                    continue
                total += remaining * k
                break
            return int(total % (1e9 + 7))

        return faster_and_smaller_storage(nums, n, left, right)
