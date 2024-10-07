from collections import deque


class Solution:
    def minLength(self, s: str) -> int:
        return self.sol1(s)

    def sol2(self, s):
        needles = {"AB", "CD"}
        pointer = 0
        while pointer < len(s):
            if s[pointer : pointer + 2] in needles:
                s = s[:pointer] + s[pointer + 2 :]
                pointer = max(0, pointer - 1)
            else:
                pointer += 1
        return len(s)

    def sol1(self, s):
        def inner(s):
            """Perform one left to right pass over string."""
            s = deque(s)
            out = ["x"]  # one letter buffer
            while s:
                char = s.popleft()
                if out[-1] + char in ["AB", "CD"]:
                    out.pop()
                    continue
                else:
                    out.append(char)
            return out[1:]

        # while True:
        #     s2 = inner(s)
        #     if s2 == s:
        #         # no changes, so stop.
        #         break
        #     s = s2
        # return len(s2)

        return len(inner(s))


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["sol1", "sol2"],
        data_file="leetcode_2696_data.txt",
        exclude_data_lines=None,
        check_result=True,
        repeat=1000,
    )
