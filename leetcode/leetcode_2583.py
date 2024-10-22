from collections import deque
from typing import List, Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def kthLargestLevelSum(self, root: Optional[TreeNode], k: int) -> int:
        """Naive solution. Visit all the nodes, starting at the root.
        Keep track of level. Add value to level sum.
        Sort level sums and return the k-1th element"""
        level_sum = [0] * (100_000 + 1)
        queue = deque([(root, 1)])
        max_level = 1
        while queue:
            node, level = queue.popleft()
            if level > max_level:
                max_level = level
            level_sum[level] += node.val
            if node.left:
                queue.append((node.left, level + 1))
            if node.right:
                queue.append((node.right, level + 1))
        if max_level < k:
            return -1
        return sorted(level_sum[1 : max_level + 1], reverse=True)[k - 1]
