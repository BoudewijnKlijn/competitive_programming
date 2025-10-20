from typing import List


class Solution:
    def finalValueAfterOperations(self, operations: List[str]) -> int:
        ans = 0
        mapping = {"X++": 1, "++X": 1, "X--": -1, "--X": -1}
        for op in operations:
            ans += mapping[op]
        return ans
