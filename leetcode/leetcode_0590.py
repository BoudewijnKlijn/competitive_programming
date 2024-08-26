from collections import deque
from typing import List


class Node:
    def __init__(self, val=None, children=None):
        self.val = val
        self.children = list()


class Solution:
    def postorder(self, root: "Node") -> List[int]:
        if not root:
            return []
        root = self.build_tree(root)
        ans = self.recursive(root, [])
        return ans

    def recursive(self, node, ans):
        for child in node.children:
            self.recursive(child, ans)

        ans.append(node.val)
        return ans

    def build_tree(self, root: List[int]) -> Node:
        tree = Node(val=root[0])
        parents = deque([tree])
        for val in root[1:]:
            if not val:
                parent = parents.popleft()
                continue

            node = Node(val=val)
            parent.children.append(node)
            parents.append(node)

        return tree


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["postorder"],
        data_file="leetcode_0590_data.txt",
        data_lines=None,
    )
