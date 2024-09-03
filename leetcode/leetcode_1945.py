class Solution:
    def getLucky(self, s: str, k: int) -> int:
        ints = []
        for char in s:
            ints.append(ord(char) - 96)

        for _ in range(k):
            total = 0
            for i in ints:
                while i:
                    i, mod = divmod(i, 10)
                    total += mod
            ints = [total]
        return total
