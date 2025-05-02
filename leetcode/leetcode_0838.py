class Solution:
    def pushDominoes(self, dominoes: str) -> str:
        n = len(dominoes)

        # determine initial push directions
        pushed_left = set()
        pushed_right = set()
        for i, direction in enumerate(dominoes):
            if direction == "L":
                pushed_left.add(i)
            elif direction == "R":
                pushed_right.add(i)

        # iterate, until all pushed over
        while pushed_right or pushed_left:
            new_pushed_left = set()
            new_pushed_right = set()
            while pushed_left:
                current = pushed_left.pop()
                left = current - 1
                # if also present in pushed_right, then it doesnt get pushed over
                if left - 1 in pushed_right:
                    pushed_right.remove(left - 1)
                    continue
                # within bounds and not pushed yet, push!
                if left >= 0 and dominoes[left] == ".":
                    dominoes = dominoes[:left] + "L" + dominoes[left + 1 :]
                    new_pushed_left.add(left)

            while pushed_right:
                current = pushed_right.pop()
                right = current + 1
                # if also present in pushed_left, then it doesnt get pushed over
                if right + 1 in pushed_left:
                    pushed_left.remove(right + 1)
                    continue
                # within bounds and not pushed yet, push!
                if right < n and dominoes[right] == ".":
                    dominoes = dominoes[:right] + "R" + dominoes[right + 1 :]
                    new_pushed_right.add(right)

            pushed_left = new_pushed_left
            pushed_right = new_pushed_right

        return dominoes


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["pushDominoes"],
        data_file="leetcode_0838_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
