from typing import List


class Solution:
    def trap(self, height: List[int]) -> int:
        """Use a stack (life queue).
        One pass. Stack is also O(n), so O(2*n) = O(n).
        Height of hill must first decrease (add it to stack) and thereafter rise.
            Compare height with last in stack.
            If higher, the remove last in stack, and take next from the stack.
            If lower or equal, stop comparing and go to next.
            If equal, remove last in stack.
        """
        prev = height[0]
        stack = list()
        ans = 0
        for idx, h in enumerate(height[1:], start=1):
            if h == prev:
                continue
            elif h < prev:
                # add to stack
                stack.append(idx - 1)
            else:
                # compare with stack
                i = len(stack) - 1
                while i >= 0:
                    height_stack = height[stack[i]]
                    ans += (min(h, height_stack) - prev) * (idx - stack[i] - 1)
                    if h >= height_stack:
                        # cannot use this stack anymore.
                        stack.pop()
                        prev = height_stack
                    if h <= height_stack:
                        break
                    i -= 1
            prev = h
        return ans


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["trap"],
        data_file="leetcode_0042_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
