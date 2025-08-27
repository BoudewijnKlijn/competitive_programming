

class Solution:
    def longestPalindrome(self, s: str) -> str:
        return self.move_outward(s)

    def move_outward(self, s):
        """Much faster for larger inputs."""
        n = len(s)
        max_len = 0
        for mid in range(n):
            for offset in [0, 1]:  # for odd and even
                start, end = mid, mid + offset
                while start >= 0 and end < n and s[start] == s[end]:
                    start -= 1
                    end += 1
                # correct for incrementing too much
                start += 1
                end -= 1
                length = end - start + 1
                if length > max_len:
                    max_len = length
                    ans = s[start : end + 1]
        return ans

    def bruteforce_fixed_length(self, s: str) -> str:
        """Try all lengths and starting positions."""
        n = len(s)
        for length in range(n, 0, -1):
            for start in range(0, n - length + 1):
                if self.is_palindrome(s[start : start + length]):
                    return s[start : start + length]

    def is_palindrome(self, string):
        n = len(string)
        mid = n // 2
        if string[:mid] != string[: -mid - 1 : -1]:
            return False
        return True


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["longestPalindrome"],
        data_file="leetcode_0005_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
