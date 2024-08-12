from bisect import bisect_left, insort
from typing import List


class KthLargest:

    # # basic
    # def __init__(self, k: int, nums: List[int]):
    #     self.sorted_nums = sorted(nums)
    #     self.k = k

    # def add(self, val: int) -> int:
    #     insort(self.sorted_nums, val)
    #     return self.sorted_nums[-self.k]

    # # less memory, but slower
    # def __init__(self, k: int, nums: List[int]):
    #     self.sorted_nums = sorted(nums)[-k:]
    #     self.k = k

    # def add(self, val: int) -> int:
    #     idx = bisect_left(self.sorted_nums, val)
    #     if len(self.sorted_nums) < self.k:
    #         self.sorted_nums.insert(idx, val)
    #     elif idx > 0:
    #         # drop the item at index 0, and insert val
    #         self.sorted_nums = self.sorted_nums[1:idx] + [val] + self.sorted_nums[idx:]
    #     return self.sorted_nums[0]

    # faster and less memory, but more complex
    # a better solution is by using heapq, which i was not familiar with.
    def __init__(self, k: int, nums: List[int]):
        self.sorted_nums = sorted(nums)[-k:]
        self.k = k
        self.kth_largest = self.sorted_nums.pop(0) if self.sorted_nums else None

    def add(self, val: int) -> int:
        if self.kth_largest is None:
            self.kth_largest = val
        elif val <= self.kth_largest:
            if len(self.sorted_nums) < self.k - 1:
                self.sorted_nums = [self.kth_largest] + self.sorted_nums
                self.kth_largest = val
        else:
            insort(self.sorted_nums, val)
            if len(self.sorted_nums) > self.k - 1:
                self.kth_largest = self.sorted_nums.pop(0)
        return self.kth_largest


# Your KthLargest object will be instantiated and called as such:
# obj = KthLargest(k, nums)
# param_1 = obj.add(val)
