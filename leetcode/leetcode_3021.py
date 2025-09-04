class Solution:
    def flowerGame(self, n: int, m: int) -> int:
        """Total must be odd.
        For each odd n, combine with even m.
        For each even n, combine with odd m."""
        odd_n = n // 2 + n % 2
        even_n = n // 2
        odd_m = m // 2 + m % 2
        even_m = m // 2
        return odd_n * even_m + even_n * odd_m
