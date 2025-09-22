from collections import defaultdict
from typing import List


class Solution:
    def maxFrequencyElements(self, nums: List[int]) -> int:
        counts = dict()
        count_counts = defaultdict(int)
        max_count = 0
        for num in nums:
            count = 0
            if num in counts:
                count = counts[num]

            count += 1
            counts[num] = count

            if count > max_count:
                max_count = count

            count_counts[count] += 1
            count_counts[count - 1] -= 1

        return count_counts[max_count] * max_count
