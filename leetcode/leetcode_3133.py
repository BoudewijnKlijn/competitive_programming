class Solution:
    def minEnd(self, n: int, x: int) -> int:
        return self.instant(n, x)

    def instant(self, n: int, x: int) -> int:
        """This problem is basically counting in binary system, without using the bits from x,
         since those bits should always be 1. The 0 bits can be used to count.
        Since we know exactly which number we want, namely n, we can express n in binary,
         then use those bits instead of all the zeros of x."""

        def get_bits(x: int) -> int:
            bits = list(map(int, bin(x)[2:]))
            return bits

        def bits_to_int(bits: list) -> int:
            ans = 0
            for i, b in enumerate(bits[::-1]):
                if b:
                    ans += 2**i
            return ans

        n_bits = get_bits(n - 1)
        x_bits = get_bits(x)
        # fill in the zero bits of x
        for i in range(len(x_bits) - 1, -1, -1):
            if not n_bits:
                break
            if x_bits[i] == 0:
                x_bits[i] = n_bits.pop()

        # use all remaining bits of n to add to x
        while n_bits:
            x_bits.insert(0, n_bits.pop())

        return bits_to_int(x_bits)

    def naive(self, n: int, x: int) -> int:
        """Bitwise and has to result in x.
        It will only result in x if all numbers have at least the same bits as x,
        possibly with additional bits.
        We get the minimum possible end value by adding the smallest possible bits.
        Time Limit Exceeded. 656 / 765 testcases passed
        """
        import itertools

        def is_correct_bits(num: int, x: int) -> int:
            return num & x == x

        def generator(x: int):
            for num in itertools.count():
                if is_correct_bits(num, x):
                    yield num

        for done, num in enumerate(generator(x), start=1):
            if done == n:
                return num


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=[
            # "naive",
            "instant"
        ],
        data_file="leetcode_3133_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
