from typing import List, Optional


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def spiralMatrix(self, m: int, n: int, head: Optional[ListNode]) -> List[List[int]]:
        # -y corresponds with the correct matrix row

        matrix = [[-1 for _ in range(n)] for _ in range(m)]
        position = complex(0, 0)
        direction = complex(1, 0)
        while True:
            # insert value at current position
            x, y = int(position.real), int(position.imag)
            matrix[-y][x] = head.val

            # test if next position is just a step ahead or a turn
            test_next_position = position + direction
            x, y = int(test_next_position.real), int(test_next_position.imag)
            if not (0 <= -y < m and 0 <= x < n) or matrix[-y][x] != -1:
                # invalid, so first turn 90 degrees and then step
                direction *= complex(0, -1)  # turn counter-clockwise
                position = position + direction
            else:
                # valid, so take the test step
                position = test_next_position

            head = head.next
            if head is None:
                # no more nodes. stop iteration
                break
        return matrix
