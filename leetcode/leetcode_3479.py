from typing import List


class Solution:
    def numOfUnplacedFruits(self, fruits: List[int], baskets: List[int]) -> int:
        return self.tree_like(fruits, baskets)

    def tree_like(self, fruits: List[int], baskets: List[int]) -> int:
        """Create tree like structure for a stack of skipped baskets.
        Time Limit Exceeded
        739 / 740 testcases passed"""

        class TreeStack:
            """Tree like structure which holds skipped baskets.
            Structure maintains order and navigates faster to larger baskets.
            Creation:
                - If right node exists, always move to right node (to maintain order).
                - Otherwise, compare value of baskets. If larger, make right node, otherwise go left.
            Lookup (filling baskets):
                - (start at the root)
                - If basket is large enough, take it.
                - If not, go to right node, if it exists. repeat.
                - binary search TODO
            Basket removal:
                - TODO
            """

            def __init__(self, n):
                self.root_id = None
                self.values = [None] * n
                self.left = [None] * n
                self.right = [None] * n
                self.parent = [None] * n
                self.n = 0

            def __str__(self):
                return f"{self.root_id=}, {self.values=}, {self.left=}, {self.right=}, {self.parent=}"

            def add(self, new_value):
                """Add new basket to structure."""
                new_idx = self.n
                self.n += 1
                self.values[new_idx] = new_value

                if self.root_id is None:
                    self.root_id = new_idx
                    return

                node = self.root_id
                while True:
                    parent_idx = node
                    # if possible move right to maintain correct order
                    if self.right[node] is not None:
                        # move right, keep iterating.
                        node = self.right[node]
                        continue

                    if new_value <= self.values[node]:
                        if self.left[node] is None:
                            # create new left node. stop iteration.
                            self.left[node] = new_idx
                            self.parent[new_idx] = parent_idx
                            break
                        else:
                            # move left, keep iterating.
                            node = self.left[node]
                    else:
                        # create new right node. stop iteration.
                        self.right[node] = new_idx
                        self.parent[new_idx] = parent_idx
                        break

                return

            def remove(self, remove_idx):
                """Remove basket from structure."""
                parent_idx = self.parent[remove_idx]
                # determine if removed basket is a left or right child.
                if parent_idx is not None:
                    is_left_child = True
                    if self.right[parent_idx] == remove_idx:
                        is_left_child = False

                replacement_idx = None
                if self.left[remove_idx] is not None:
                    replacement_idx = self.left[remove_idx]

                    if self.right[remove_idx] is not None:
                        # connect the right node of node that will be removed, to
                        #   the rightmost node of the replacement node
                        # we know it must be larger than everything from left node
                        # follow the right nodes until no right node
                        idx = self.left[remove_idx]
                        while self.right[idx] is not None:
                            idx = self.right[idx]
                        self.right[idx] = self.right[remove_idx]
                        self.parent[self.right[remove_idx]] = idx

                elif self.right[remove_idx] is not None:
                    replacement_idx = self.right[remove_idx]

                if replacement_idx is not None:
                    # set new parent for replacement (remove_idx was previous parent)
                    self.parent[replacement_idx] = parent_idx

                    # set new child for parent (remove_idx was previous child)
                    if parent_idx is not None:
                        if is_left_child:
                            self.left[parent_idx] = replacement_idx
                        else:
                            self.right[parent_idx] = replacement_idx
                    else:
                        # no parent, set new root id
                        self.root_id = replacement_idx

                else:
                    # no replacement. remove child from parent.
                    if parent_idx is not None:
                        if is_left_child:
                            self.left[parent_idx] = None
                        else:
                            self.right[parent_idx] = None
                    else:
                        self.root_id = None
                return

            def find(self, fruit_value) -> bool:
                """Find a basket to place the fruit.
                Return whether successfull.
                Remove basket if fruit was placed."""
                if self.root_id is None:
                    # structure is empty.
                    return False

                idx = self.root_id
                # TODO: add binary search
                # for binary search, the increasing order in top level always right node needs to be maintained
                # which is not the case now. after removing a node, more nodes need to be reconnected.
                while True:
                    if fruit_value <= self.values[idx]:
                        # found basket which is large enough.
                        # remove basket from structure.
                        self.remove(idx)
                        return True
                    elif self.right[idx] is not None:
                        # find a larger basket, if possible (move to the right).
                        idx = self.right[idx]
                    else:
                        # basket is not large enough and no larger baskets in structure.
                        return False

        n = len(baskets)
        queue = TreeStack(n)
        ans = 0
        basket_i = 0
        for fruit in fruits:
            # first check the baskets in the queue.
            placed = queue.find(fruit)
            # if no match then continue with never seen baskets
            while not placed and basket_i < n:
                basket = baskets[basket_i]
                if fruit <= basket:
                    placed = True
                else:
                    queue.add(basket)
                basket_i += 1
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
            # "smarter_baskets",
            "tree_like",
        ],
        data_file="leetcode_3479_data.txt",
        exclude_data_lines=[6],
        check_result=True,
    )
