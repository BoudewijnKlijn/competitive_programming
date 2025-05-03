from typing import List


class Solution:
    def minDominoRotations(self, tops: List[int], bottoms: List[int]) -> int:
        def rotations_if_number_top(ts, bs, number):
            rot = 0
            for t, b in zip(ts, bs):
                if t == number:
                    continue
                elif b == number:
                    rot += 1
                else:
                    return -1
            return rot

        # the number is either the first of tops or the first of bottoms
        # they number may be all the same in top or bottom
        best = -1
        for n in [tops[0], bottoms[0]]:
            rot = rotations_if_number_top(tops, bottoms, n)
            if rot > -1 and (best == -1 or (best > -1 and rot < best)):
                best = rot
            # switch tops and bottoms
            rot = rotations_if_number_top(bottoms, tops, n)
            if rot > -1 and (best == -1 or (best > -1 and rot < best)):
                best = rot

        return best


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["minDominoRotations"],
        data_file="leetcode_1007_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
