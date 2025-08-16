class Solution:
    def maximum69Number(self, num: int) -> int:
        """Find first 6 and replace it with a 9."""
        string = list(str(num))
        for i, char in enumerate(string):
            if char == "6":
                string[i] = "9"
                break

        return int("".join(string))
