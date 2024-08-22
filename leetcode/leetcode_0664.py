from collections import Counter


class Solution:
    def strangePrinter(self, s: str) -> int:
        """Global minimum = 1.
        Minimum for some input is the number of unique characters in the input.
        Maximum = 100.
        One character can be printed on all places. Sort of to make a canvas.
        Then, characters on top to remove the canvas, sort of similar to altitude lines on a map.
        Except that lines can be skipped in this case (on the way up or down).
        It's all about letter changes.
        If identical numbers are next to each other, that can be simplified to a single.
        I can split the input string on a character, and then solve the created "islands".
        The "islands" can be solved independently and are subproblems of the original problem, but can be
        solved in the same way.
        The islands idea is not entirely correct. Somtimes multiple island can be solved together,
        which yields a better result. E.g. "adcacda" can be solved in 4 steps, but the islands splitting
        approach thinks it needs 5 steps.
        """
        # simplify string: remove identical characters next to each other
        simple = s[0]
        for char in s[1:]:
            if char != simple[-1]:
                simple += char

        mem = {"": 0, **{char: 1 for char in simple}}

        def inner(s):
            if s in mem:
                return mem[s]

            c = Counter(s)
            assert len(c) > 1, "counter should always have more than one key."

            ans = 100
            for split_char in c.keys():
                ans = min(ans, 1 + sum(inner(split) for split in s.split(split_char)))

            mem[s] = ans
            return ans

        return inner(simple)


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["strangePrinter"],
        data_file="leetcode_0664_data.txt",
        data_lines=[0, 1, 2, 3, 4],
    )
