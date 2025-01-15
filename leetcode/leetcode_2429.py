class Solution:
    def minimizeXor(self, num1: int, num2: int) -> int:
        # the smallest result after XOR would be all zeros.
        # to get that result, the number to use would be num1, because num1 ^ num1 = 0
        # we can only do this when num1 and num2 have same number of set bits
        # if num1 and num2 do not have the same number of bits:
        #  if num2 more bits than num1: replace zeros from the right
        #  if num2 less bits than num1: keep ones from the left
        set_bits1 = self.get_set_bits(num1)
        set_bits2 = self.get_set_bits(num2)
        if set_bits1 == set_bits2:
            return num1
        elif set_bits2 > set_bits1:
            set_bits2 -= set_bits1
            ans = bin(num1)
            i = len(ans) - 1
            while set_bits2 > 0:
                # replace zeros from the right
                if ans[i] == "b":
                    ans = ans[: i + 1] + "1" + ans[i + 1 :]
                    set_bits2 -= 1
                    continue
                elif ans[i] == "0":
                    ans = ans[:i] + "1" + ans[i + 1 :]
                    set_bits2 -= 1
                i -= 1
            return int(ans, 2)
        else:
            binary = bin(num1)[2:]
            ans = "0b"
            while set_bits2 > 0:
                add = binary[0]
                binary = binary[1:]
                if add == "1":
                    set_bits2 -= 1
                ans += add
            # all set bits used. add zeros to get same length as num1
            return int(ans + "0" * len(binary), 2)

    def get_set_bits(self, n):
        return bin(n).count("1")


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["minimizeXor"],
        data_file="leetcode_2429_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
