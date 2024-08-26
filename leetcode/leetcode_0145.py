from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def postorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        if not root:
            return []
        return self.recursive(root, [])

    def recursive(self, node, ans):
        if node.left:
            self.recursive(node.left, ans)
        if node.right:
            self.recursive(node.right, ans)
        ans.append(node.val)
        return ans
