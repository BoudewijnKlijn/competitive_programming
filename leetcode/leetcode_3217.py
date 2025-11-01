from typing import List, Optional


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def modifiedList(
        self, nums: List[int], head: Optional[ListNode]
    ) -> Optional[ListNode]:
        nums = set(nums)
        # find the first number that is not in nums. this will be the head we return.
        while head.val in nums:
            head = head.next

        # remove all the nodes after head which value is present in nums
        tmp = head.next
        last = head
        while tmp:
            if tmp.val not in nums:
                last.next = tmp
                last = last.next
            tmp = tmp.next
        last.next = None
        return head
