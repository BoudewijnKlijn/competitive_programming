class Solution:
    def shortestPalindrome(self, s: str) -> str:
        """Assume a length of the palindrome
        Based on this length determine the part before and after the midpoint
        Compare both, but only use as much characters as in the before part
        Reconstruct with extra characters from the after part"""
        n = len(s)
        if n < 2:
            return s

        assumed_length = n
        while True:
            half, odd = divmod(assumed_length, 2)
            after = s[-half:]
            before = s[: -half - odd]
            n_before = len(before)
            if before == after[:n_before][::-1]:
                if odd:
                    return after[::-1] + s[-half - 1] + after
                return after[::-1] + after
            assumed_length += 1


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["shortestPalindrome"],
        data_file="leetcode_0214_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
