from typing import List


class Solution:
    def numOfUnplacedFruits(self, fruits: List[int], baskets: List[int]) -> int:
        return self.tree_like(fruits, baskets)

    def tree_like(self, fruits: List[int], baskets: List[int]) -> int:
        """Create tree like structure for the baskets.
        The head is the first basket.
        The second basket becomes the left node of the head if less than or equal to head
            and right node if larger than value of head.
        If the right node has a value, always go to the right node, before adding new nodes.
        The third basket becomes the right node of the right node,
            or the left or right node of the left node. Etc.
        Then fruits are allocated to baskets.
        Once basket is found, its left node takes its place and the right node is appended
            to the ultimate right ... right node of the left node.

        Can add binary search, which helps for large values, but not for testcase 737 where all values are identical.
        Time Limit Exceeded
        737 / 740 testcases passed"""

        class Node:
            def __init__(self, value):
                self.value = value
                self.left = None
                self.right = None

        # create structure
        root = Node(baskets[0])
        for basket in baskets[1:]:
            node = root
            while True:
                # if right exists, go right, to maintain order
                if node.right is not None:
                    node = node.right
                    continue

                if basket <= node.value:
                    if node.left is None:
                        node.left = Node(basket)
                        break
                    else:
                        node = node.left
                else:
                    node.right = Node(basket)
                    break

        # check fruits and update structure
        ans = 0
        for fruit in fruits:
            parent = None
            node = root
            placed = False
            while node is not None:
                if fruit > node.value:
                    parent = node
                    node = node.right
                    continue

                # found basket which is large enough
                placed = True
                # update structure
                # left node always takes place of node, if it exists.
                # connect right node to rightmost node of left.
                # this way order is maintained and also skip to large numbers quickly.
                replacement = node.left
                if replacement is None:
                    replacement = node.right
                else:
                    tmp = node.right
                    node = replacement
                    while node.right is not None:
                        node = node.right
                    node.right = tmp

                if parent is None:
                    root = replacement
                else:
                    parent.right = replacement
                break

            if not placed:
                ans += 1
        return ans

    def create_smart_baskets(self, baskets, smart_baskets=None):
        """List with lists.
        First item of each list is strictly higher than that of previous list.
        Remainder of each list is less than or equal to first item,
            and otherwise in order of original appearance.
        """
        if smart_baskets is None:
            smart_baskets = list()

        for basket in baskets:
            if len(smart_baskets) == 0 or basket > smart_baskets[-1][0]:
                smart_baskets.append([basket])  # new top level
            else:
                smart_baskets[-1].append(basket)
        return smart_baskets

    def smarter_baskets(self, fruits: List[int], baskets: List[int]) -> int:
        """If a basket with some values comes after a basket with a higher basket, it will not be used.
        By using a list with lists, the baskets can be looped over more efficiently.
        Place smaller buckets in a list with the larger basket, and only check the first.
        After using a basket, the underlying bucketss should be replaced.

        Possible to improve further with binary search on smart buckets,
            but that wont help to improve time on testcase 737.
        Time Limit Exceeded
        737 / 740 testcases passed
        """
        smart_baskets = self.create_smart_baskets(baskets)
        ans = 0
        for fruit in fruits:
            placed = False
            for basket_i, baskets in enumerate(smart_baskets):
                if baskets[0] >= fruit:
                    # update bucket structure without first bucket and redistributing remainder
                    smart_baskets = (
                        self.create_smart_baskets(
                            baskets[1:],
                            smart_baskets=smart_baskets[:basket_i],
                        )
                        + smart_baskets[basket_i + 1 :]
                    )
                    placed = True
                    break
            if not placed:
                ans += 1
        return ans

    def brute_force(self, fruits: List[int], baskets: List[int]) -> int:
        """Identical to leetcode 3477.
        Time Limit Exceeded
        732 / 740 testcases passed"""
        used = set()
        ans = 0
        for fruit in fruits:
            for basket_i, size in enumerate(baskets):
                if fruit <= size and basket_i not in used:
                    used.add(basket_i)
                    break
            else:
                ans += 1
        return ans


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=[
            # "numOfUnplacedFruits",
            # "brute_force",
            "smarter_baskets",
            "tree_like",
        ],
        data_file="leetcode_3479_data.txt",
        exclude_data_lines=[5],
        check_result=True,
    )
