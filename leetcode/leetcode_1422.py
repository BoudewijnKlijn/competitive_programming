class Solution:
    def maxScore(self, s: str) -> int:
        return self.faster(s)

    def faster(self, s: str) -> int:
        n_ones = s.count("1")
        max_score = 0
        score = n_ones
        for char in s[:-1]:
            if char == "0":
                score += 1
            else:
                score -= 1
            max_score = max(max_score, score)
        return max_score

    def naive(self, s: str) -> int:
        max_score = 0
        for split_id in range(1, len(s)):
            left = s[:split_id]
            right = s[split_id:]
            score = left.count("0") + right.count("1")
            if score > max_score:
                max_score = score
        return max_score


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["naive", "one_pass"],
        data_file="leetcode_1422_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
