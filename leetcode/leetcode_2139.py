

class Solution:
    def minMoves(self, target: int, maxDoubles: int) -> int:
        """Its always best to increment first, since both yield the same, but doubling is limited.
        Its always best to double later, rather than sooner if we hit the double limit, because
            doubling later gains more.
        """
        moves = 0
        while target > 1:
            div, mod = divmod(target, 2)
            if maxDoubles > 0 and not mod:
                target = div
                maxDoubles -= 1
                moves += 1
            elif not maxDoubles:
                target = 1
                moves += target - 1
            else:
                target -= 1
                moves += 1
        return moves


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["minMoves"],
        data_file="leetcode_2139_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
