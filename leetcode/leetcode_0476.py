class Solution:
    def findComplement(self, num: int) -> int:
        return self.mult2(num)

    def pow(self, num: int) -> int:
        som = 0
        power = 0
        while som < num:
            som += 2**power
            power += 1

        return 2**power - 1 - num

    def div2(self, num: int) -> int:
        n = num
        power = 0
        while num:
            num //= 2
            power += 1
        return 2**power - 1 - n

    def mult2(self, num: int) -> int:
        som = 1
        while som <= num:
            som *= 2
        return som - 1 - num

    def bitshift(self, num: int) -> int:
        som = 1
        while som <= num:
            som = som << 1
        return som - 1 - num

    def xor_leetcode(self, num: int) -> int:
        """From leetcode forum; is faster than mine."""
        bit_length = num.bit_length()
        mask = (1 << bit_length) - 1
        return num ^ mask


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["pow", "div2", "mult2", "bitshift", "xor_leetcode"],
        data_file="leetcode_0476_data.txt",
        data_lines=None,
        repeat=1000,
    )
