from collections import Counter


class Solution:
    def minimumPushes(self, word: str) -> int:
        c = Counter(word)

        ans = 0
        mult = 1
        i = 0
        for _, v in c.most_common():
            ans += v * mult
            i += 1
            if i % 8 == 0:
                mult += 1
                i = 0
        return ans
