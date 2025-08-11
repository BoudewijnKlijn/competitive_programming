import os


def solve():
    def abbreviate(word):
        return word[0] + str(len(word) - 2) + word[-1]

    n_words = int(input())
    for _ in range(n_words):
        word = input()
        if len(word) <= 10:
            print(word)
        else:
            print(abbreviate(word))


if __name__ == "__main__":
    MULTIPLE_TESTS = False
    if not os.path.exists("LOCAL"):
        t = 1
        if MULTIPLE_TESTS:
            t = int(input())
        for _ in range(t):
            solve()
    else:
        import test_runner

        test_runner.main(solve, __file__, MULTIPLE_TESTS)
