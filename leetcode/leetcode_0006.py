

class Solution:
    def convert(self, s: str, numRows: int) -> str:
        """Column doesnt matter."""
        if numRows == 1:
            return s

        idx, row = 0, 0
        n = len(s)
        out = ["" for _ in range(numRows)]
        while idx < n:

            char = s[idx]
            out[row] += char
            idx += 1

            if row == 0:
                dr = 1
            elif row == numRows - 1:
                dr = -1

            row += dr

        return "".join(out)


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["convert"],
        data_file="leetcode_0006_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
