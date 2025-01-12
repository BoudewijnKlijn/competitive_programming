class Solution:
    def canBeValid(self, s: str, locked: str) -> bool:
        # odd length can never be correct
        if len(s) % 2:
            return False

        def check(s, locked, reverse=False):
            if reverse:
                locked = locked[::-1]
                s = s[::-1].replace("(", "x").replace(")", "(").replace("x", ")")
            # loop over the string once
            # an excessive closing brackets can be converted to opening if not locked
            open_closed_tally = 0  # should never be < 0
            margin = 0
            for char, locked_char in zip(s, locked):
                if char == "(":
                    open_closed_tally += 1
                else:
                    open_closed_tally -= 1
                    margin += 1 - int(locked_char)

                if open_closed_tally < 0:
                    margin -= 1
                    if margin < 0:
                        return False
                    open_closed_tally += 2

            return True

        return check(s, locked) and check(s, locked, reverse=True)


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["canBeValid"],
        data_file="leetcode_2116_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
