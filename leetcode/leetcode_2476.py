from typing import List, Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def closestNodes(
        self, root: Optional[TreeNode], queries: List[int]
    ) -> List[List[int]]:
        """Sort queries. Remember original index.
        Get all values from binary tree in sorted order.
        Do one pass over both arrays with two pointers.
        Insert each answer at correct index.
        """

        def search(node, values):
            if node.left:
                values = search(node.left, values)
            values.append(node.val)
            if node.right:
                values = search(node.right, values)
            return values

        # Sort queries. Keep original index.
        sorted_queries = sorted(enumerate(queries), key=lambda x: x[1])
        tree_values = search(root, [])

        tree_pointer = 0
        ans = [None] * len(sorted_queries)
        prev = None
        for idx, query in sorted_queries:
            while (
                tree_pointer < len(tree_values) and tree_values[tree_pointer] <= query
            ):
                prev = tree_values[tree_pointer]
                tree_pointer += 1

            # store answer at original index.
            ans[idx] = (
                # the min value is always prev because pointer increases up to and including,
                # except when prev is None
                (-1 if prev is None else prev),
                # the max value might be prev, and otherwise the current value if pointer is still
                # in range, and if out of range then its not present (-1)
                (
                    prev
                    if prev == query
                    else (
                        tree_values[tree_pointer]
                        if tree_pointer < len(tree_values)
                        else -1
                    )
                ),
            )

        return ans
