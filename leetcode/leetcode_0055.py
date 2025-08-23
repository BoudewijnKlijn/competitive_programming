from typing import List


class Solution:
    def canJump(self, nums: List[int]) -> bool:
        return self.one_pass(nums)

    def one_pass(self, nums: List[int]) -> bool:
        """We need enough resources to move forward and get over zeros.
        If not enough resources than return False.
        Decrease resources every step.
        Increase resources when we encounter a larger jump value, which may
            get us over later zeros.
        """
        resources = 1
        for num in nums:
            resources -= 1
            if resources < 0:
                return False
            if num != 0 and num > resources:
                resources = num
        return True

    def recursion(self, nums: List[int]) -> bool:
        """Recursion"""

        def inner_jump(idx):
            if idx >= n - 1:
                return True

            # jump as far as possible. thereafter try smaller jumps
            for jump_length in range(nums[idx], 0, -1):
                new_idx = idx + jump_length
                if new_idx in seen:
                    continue
                if inner_jump(new_idx):
                    return True
            seen.add(idx)
            return False

        seen = set()
        n = len(nums)
        return inner_jump(0)

    def using_heap(self, nums: List[int]) -> bool:
        import heapq

        negative_positions = [0]
        seen = set()
        n = len(nums)
        while negative_positions:
            pos = -heapq.heappop(negative_positions)
            if pos >= n - 1:
                return True
            seen.add(pos)
            for jump in range(1, nums[pos] + 1):
                if pos + jump in seen:
                    continue
                heapq.heappush(negative_positions, -(pos + jump))

        return False


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["using_heap", "recursion", "one_pass"],
        data_file="leetcode_0055_data.txt",
        exclude_data_lines=[0],
        check_result=True,
    )
