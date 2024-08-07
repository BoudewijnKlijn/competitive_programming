class Solution:
    def numberToWords(self, num: int) -> str:
        if num == 0:
            return "Zero"
        digits_to_words = {
            1: "One",
            2: "Two",
            3: "Three",
            4: "Four",
            5: "Five",
            6: "Six",
            7: "Seven",
            8: "Eight",
            9: "Nine",
            10: "Ten",
            11: "Eleven",
            12: "Twelve",
            13: "Thirteen",
            14: "Fourteen",
            15: "Fifteen",
            16: "Sixteen",
            17: "Seventeen",
            18: "Eighteen",
            19: "Nineteen",
            20: "Twenty",
            30: "Thirty",
            40: "Forty",
            50: "Fifty",
            60: "Sixty",
            70: "Seventy",
            80: "Eighty",
            90: "Ninety",
            100: "Hundred",
        }
        level = 0
        words_in_reverse_order = []
        while num:
            num, mod = divmod(num, 10)

            prev_num = 0
            if words_in_reverse_order:
                _, prev_num = words_in_reverse_order[-1]
                print(level, prev_num, words_in_reverse_order)
            if level in [2, 5, 8]:
                words_in_reverse_order.append(("Hundred", 100))
            elif level == 3:
                if prev_num == 100:
                    words_in_reverse_order.pop()
                words_in_reverse_order.append(("Thousand", 1e3))
            elif level == 6:
                if prev_num == 1e3:
                    words_in_reverse_order.pop()
                words_in_reverse_order.append(("Million", 1e6))
            elif level == 9:
                if prev_num == 1e6:
                    words_in_reverse_order.pop()
                words_in_reverse_order.append(("Billion", 1e9))

            if mod == 0:
                if words_in_reverse_order:
                    _, prev_num = words_in_reverse_order[-1]
                if prev_num == 100:
                    words_in_reverse_order.pop()
                level += 1
                continue

            if level in [0, 3, 6, 9]:
                words_in_reverse_order.append((digits_to_words[mod], mod))
            elif level in [1, 4, 7, 10]:
                if mod == 1:
                    if words_in_reverse_order:
                        _, prev_num = words_in_reverse_order[-1]
                    prev_num = prev_num % 10
                    if prev_num:
                        words_in_reverse_order.pop()
                    words_in_reverse_order.append(
                        (digits_to_words[10 + prev_num], 10 + prev_num)
                    )
                if mod > 1:
                    words_in_reverse_order.append((digits_to_words[mod * 10], mod * 10))
            elif level in [2, 5, 8, 11]:
                if mod >= 1:
                    words_in_reverse_order.append((digits_to_words[mod], mod))

            level += 1
        return " ".join(
            (w for w, _ in words_in_reverse_order[::-1] if w.strip())
        ).strip()


arr = range(100)
# arr = [0, 100, 1e3, 9e3, 1e4, 9e4, 1e5, 9e5, 1e6, 1234567891]
for i in arr:
    print(i, Solution().numberToWords(i))
