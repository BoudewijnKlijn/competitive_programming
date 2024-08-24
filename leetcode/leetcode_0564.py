class Solution:
    def str_is_palinedrome(self, s: str) -> bool:
        return s == s[::-1]

    def nearestPalindromic(self, n: str) -> str:
        n_int = int(n)
        if n_int <= 10:
            return str(n_int - 1)

        if len(n) < 3:
            n_int_min, n_int_plus = n_int, n_int
            while True:
                n_int_min -= 1
                if self.str_is_palinedrome(str(n_int_min)):
                    return str(n_int_min)
                n_int_plus += 1
                if self.str_is_palinedrome(str(n_int_plus)):
                    return str(n_int_plus)

        options = list()  # tuples with (abs diff, int palinedrome)

        def add_option(first_half: str, mid_char: str) -> None:
            palindrome = first_half + mid_char + first_half[::-1]
            palindrome_int = int(palindrome)
            diff = abs(n_int - palindrome_int)
            if diff != 0:
                options.append((diff, palindrome_int))

        length = len(n)
        is_odd = length % 2
        mid = length // 2

        if is_odd:
            tmp = n[: mid + 1]  # include the mid character
            for diff in [-1, 0, 1]:
                tmp_int = int(tmp) + diff
                has_different_n_digits = len(str(tmp_int)) != mid + 1
                if has_different_n_digits:
                    add_option(str(tmp_int)[: mid + 1], "")
                else:
                    add_option(str(tmp_int)[:mid], str(tmp_int)[-1])
        else:
            tmp = n[:mid]
            for diff in [-1, 0, 1]:
                tmp_int = int(tmp) + diff
                has_different_n_digits = len(str(tmp_int)) != mid
                if has_different_n_digits:
                    add_option(str(tmp_int)[:mid], str(tmp_int)[-1])
                else:
                    add_option(str(tmp_int), "")

        return str(min(options)[1])


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["nearestPalindromic"],
        data_file="leetcode_0564_data.txt",
        data_lines=None,
        check_result=True,
    )
