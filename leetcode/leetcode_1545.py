class Solution:
    def findKthBit(self, n: int, k: int) -> str:
        """Naive"""

        def invert(s):
            new = ""
            for char in s:
                if char == "1":
                    new += "0"
                else:
                    new += "1"
            return new

        s = "0"
        for _ in range(n - 1):
            s = s + "1" + invert(s)[::-1]
        return s[k - 1]


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["findKthBit"],
        data_file="leetcode_1545_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
