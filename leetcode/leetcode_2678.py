import timeit
from typing import List


class Solution:

    def countSeniors(self, details: List[str]) -> int:
        return sum(int(d[11:13]) > 60 for d in details)


def f1(details):
    return sum(int(d[11:13]) > 60 for d in details)


# alternatives but more convoluted and not faster


def f11(details):
    return sum(int(d11 + d12) > 60 for *_, d11, d12, _, _ in details)


def f2(details):
    return sum(
        int(d11) > 6 or (d11 == "6" and d12 != "0") for *_, d11, d12, _, _ in details
    )


def f3(details):
    good = {"7", "8", "9"}
    return sum(
        d11 in good or (d11 == "6" and d12 != "0") for *_, d11, d12, _, _ in details
    )


def f4(details):
    *_, d11, d12, _, _ = zip(*details)
    return sum(
        int(d11) > 6 or (d11 == "6" and d12 != "0") for d11, d12 in zip(d11, d12)
    )


# time the different solutions
details = [
    "7868190130M0522",
    "7868190130M1522",
    "7868190130M2522",
    "7868190130M3522",
    "7868190130M4522",
    "7868190130M5522",
    "7868190130M6522",
    "7868190130M7522",
    "7868190130M8522",
    "7868190130M9522",
] * 10

funcs = [f1, f11, f2, f3, f4]
for f in funcs:
    print(
        timeit.repeat(
            "f(details)",
            globals={"f": f, "details": details},
            number=10_000,
            repeat=3,
        )
    )
