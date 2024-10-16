class Solution:
    def longestDiverseString(self, a: int, b: int, c: int) -> str:
        """Ugly solution :("""

        ans = ""
        while True:
            allowed = {"a", "b", "c"}
            disallowed = set()
            for char in allowed:
                if eval(char) == 0:
                    disallowed.add(char)
                elif len(ans) > 1 and ans[-1] == ans[-2] == char:
                    disallowed.add(char)
            tmp = allowed - disallowed
            if tmp:
                max_ = 0
                for char in tmp:
                    if eval(char) > max_:
                        add = char
                        max_ = eval(char)
                ans += add

                if add == "a":
                    a -= 1
                elif add == "b":
                    b -= 1
                elif add == "c":
                    c -= 1
                continue
            break
        return ans
