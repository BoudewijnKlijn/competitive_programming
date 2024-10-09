class Solution:
    def minAddToMakeValid(self, s: str) -> int:
        """Loop from left to right over string.
        If encounter ( add 1, if encounter ) subtract 1.
        If the running sum dips below zero, then that cannot be fixed later, so ans +1
        If running sum ends above zero, then we add that to the ans as well."""
        char_val = {"(": 1, ")": -1}
        running_total = 0
        ans = 0
        for char in s:
            running_total += char_val[char]
            if running_total < 0:
                ans += 1
                running_total = 0
        ans += running_total
        return ans


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["minAddToMakeValid"],
        data_file="leetcode_0921_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
