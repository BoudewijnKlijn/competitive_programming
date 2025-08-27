
roman_dict = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}


class Solution:
    def romanToInt(self, s: str) -> int:
        prev = s[0]
        ans = roman_dict[prev]
        for char in s[1:]:
            if prev == "I" and char in "VX":
                ans -= 2
            elif prev == "X" and char in "LC":
                ans -= 20
            elif prev == "C" and char in "DM":
                ans -= 200
            prev = char
            ans += roman_dict[char]
        return ans


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["romanToInt"],
        data_file="leetcode_0013_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
