import heapq
from typing import List


class Solution:
    def findUnsortedSubarray(self, nums: List[int]) -> int:
        return self.one_pass(nums)

    def one_pass(self, nums: List[int]) -> int:
        """One pass over numbers. Store minimum and maximum numbers which are in wrong place.
        Thereafter another pass from left and right to correct for duplicate values of
            minimum and maximum.
        8ms Beats 76.51%
        """
        minimum = 100_001
        maximum = -100_001
        prev = nums[0]
        for num in nums[1:]:
            if num < prev:
                minimum = min(minimum, num)
                maximum = max(maximum, prev)
            prev = num

        if minimum == 100_001:
            return 0

        start = 0
        while nums[start] <= minimum:
            start += 1

        end = len(nums) - 1
        while nums[end] >= maximum:
            end -= 1

        return end - start + 1

    def min_max_heap(self, nums: List[int]) -> int:
        """Not faster than sorting everything.
        Put numbers in min and max heap.
        Then pull out number until index doesn't match.
        Could be faster, because:
            - Can stop once mismatch
            - Complete and precise order not necessary
        87ms Beats 5.21%
        """
        add = 100_001  # such that all values are positive
        n = len(nums)
        min_heap = []
        max_heap = []
        # put all values in min_heap and max_heap
        for i, num in enumerate(nums):
            heapq.heappush(min_heap, (num + add, i))
            heapq.heappush(
                max_heap, (-(num + add), n - i - 1)
            )  # minus such that max is pulled out first. index from the back

        def pull(heap):
            """Pull out values until mismatch."""
            i = 0
            while heap:
                _, idx = heapq.heappop(heap)
                if idx != i:
                    break
                i += 1
            return i

        i = pull(min_heap)
        j = n - 1 - pull(max_heap)

        if j < i:
            return 0
        return j - i + 1

    def determine_correct_order(self, nums: List[int]) -> int:
        """Slow.
        Numbers which are in the correct place can be excluded."""
        n = len(nums)
        if n < 2:
            return 0

        # determine correct place
        order = sorted(zip(nums, range(n)))

        start = n

        for i, (_, orig_idx) in enumerate(order):
            if i != orig_idx:
                # if not correct place, store smallest
                start = min(start, orig_idx)

        # everything in correct place, return ans
        if start == n:
            return 0

        end = -1
        for j, (_, orig_idx) in enumerate(reversed(order)):

            if j != n - 1 - orig_idx:
                # if not correct place, store largest
                end = max(end, orig_idx)

        return end - start + 1


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=[
            # "findUnsortedSubarray",
            "determine_correct_order",
            "min_max_heap",
            "one_pass",
        ],
        data_file="leetcode_0581_data.txt",
        exclude_data_lines=None,
        repeat=100,
        check_result=True,
    )
