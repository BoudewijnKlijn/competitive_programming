from typing import List


class Solution:
    def lemonadeChange(self, bills: List[int]) -> bool:
        change = {5: 0, 10: 0}
        for b in bills:
            match b:
                case 5:
                    change[b] += 1
                case 10:
                    change[5] -= 1
                    if change[5] < 0:
                        return False
                    change[b] += 1
                case 20:
                    if change[10] > 0:
                        change[10] -= 1
                        change[5] -= 1
                    else:
                        change[5] -= 3
                    if change[5] < 0:
                        return False
        return True
