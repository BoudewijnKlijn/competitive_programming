import math
from typing import Optional


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def insertGreatestCommonDivisors(
        self, head: Optional[ListNode]
    ) -> Optional[ListNode]:
        node = head
        while node.next:
            # determine insert value
            current_val = node.val
            next_val = node.next.val
            insert_val = math.gcd(current_val, next_val)

            # insert node
            node.next = ListNode(val=insert_val, next=node.next)

            # go to node after the inserted node
            node = node.next.next
        return head
