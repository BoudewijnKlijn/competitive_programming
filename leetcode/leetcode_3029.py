

class Solution:
    def minimumTimeToInitialState(self, word: str, k: int) -> int:
        """Replace k from the front and add characters at end.
        Removing the complete word and replacing with new is the obvious upper limit.
            So ans = 1 + n // k if n % k else n // k
        A better result can be achieved if the start and end have the same characters AND
            if removing a multiple of k ends precisly from where start and end match.
        """
        n = len(word)
        if k == n:
            return 1

        div, mod = divmod(n, k)
        # by choosing start=mod and k as stepsize we eliminate the check: (n - length) % k == 0:
        # by going in reverse direction, we go from optimal to worse possible answers, so can return immediately.
        for length in range(mod + (div - 1) * k, 0, -k):
            if word[:length] == word[-length:]:  # and (n - length) % k == 0:
                return (n - length) // k
        return 1 + div if mod else div


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["minimumTimeToInitialState"],
        data_file="leetcode_3029_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
