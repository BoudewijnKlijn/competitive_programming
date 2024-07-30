class Solution:
    def minimumDeletions(self, s: str) -> int:
        # loop over array and check how many b's are to left, and a's to right.
        # sum is how many you would need to remove
        # take minimum

        def count_char_to_left(s, char):
            counts = [0] * len(s)
            n = 0
            for i, ss in enumerate(s):
                counts[i] = n
                if ss == char:
                    n += 1
            return counts

        b_left = count_char_to_left(s, "b")
        a_right = count_char_to_left(s[::-1], "a")[::-1]

        total = [a + b for a, b in zip(a_right, b_left)]
        return min(total)
