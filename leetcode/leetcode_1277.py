from typing import List


class Solution:
    def countSquares(self, matrix: List[List[int]]) -> int:
        """Count ones, then shrink matrix by 1 in horizontal and vertical direction, then repeat.
        New matrix square becomes 1 if all neighbors are 1, else 0.
        If square is 1 after transforming once, that was a 2-side square.
        If square is 1 after transforming twice, that was a 3-side square. Etc.

        It's like a convolutional layer.
        Not optimal since regions with zeros are still propagated."""
        NEIGHBORS = [(0, 0), (0, 1), (1, 0), (1, 1)]

        def shrink(mat):
            """Change matrix in place."""
            m, n = len(mat), len(mat[0])
            for mm in range(m - 1):
                for nn in range(n - 1):
                    for dm, dn in NEIGHBORS:
                        if mat[mm + dm][nn + dn] != 1:
                            mat[mm][nn] = 0
                            break
                    else:
                        mat[mm][nn] = 1
            # return reduced size
            return [row[:-1] for row in mat[:-1]]

        ans = 0
        while True:
            add = sum(map(sum, matrix))
            ans += add
            if add:
                matrix = shrink(matrix)
            else:
                return ans


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["countSquares"],
        data_file="leetcode_1277_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
