class Solution(object):
    def buildMatrix(self, k, rowConditions, colConditions):
        """
        :type k: int
        :type rowConditions: List[List[int]]
        :type colConditions: List[List[int]]
        :rtype: List[List[int]]
        """
        # return [[0, 0, 0],
        #         [3, 0, 1],
        #         [0, 2, 0]]
        # sort left (highest) to right
        # sort top (highest) to bottom
        # then place numbers on places where they intersect

        def sort(k, x):
            failed = set()
            position_of = {i: i - 1 for i in range(1, k + 1)}
            number_at = {i - 1: i for i in range(1, k + 1)}

            def make_order():
                return tuple(number_at.values())

            try_again = True
            while try_again:
                order = make_order()
                for above, below in x:
                    if position_of[above] < position_of[below]:
                        continue

                    # add order to failed set
                    if order in failed:
                        try_again = False
                        break
                    failed.add(order)

                    # switch position simultaneously and try again
                    (
                        position_of[above],
                        position_of[below],
                    ) = (position_of[below], position_of[above])
                    number_at[position_of[above]], number_at[position_of[below]] = (
                        above,
                        below,
                    )
                    break
                else:
                    break

            return try_again, position_of

        row_possible = sort(k, rowConditions)
        col_possible = sort(k, colConditions)

        def combine(pos_row, pos_col):
            base = [[0 for _ in range(k)] for _ in range(k)]
            for number in range(1, k + 1):
                row, col = pos_row[number], pos_col[number]
                base[row][col] = number
            return base

        if row_possible[0] and col_possible[0]:
            ans = combine(row_possible[1], col_possible[1])
            return ans
        return list()
