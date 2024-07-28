import pytest

from leetcode_2045 import Solution


@pytest.mark.parametrize(
    "n,edges,time,change,expected",
    [
        (5, [[1, 2], [1, 3], [1, 4], [3, 4], [4, 5]], 3, 5, 13),
        (
            12,
            [
                [1, 2],
                [1, 3],
                [3, 4],
                [2, 5],
                [4, 6],
                [2, 7],
                [1, 8],
                [5, 9],
                [3, 10],
                [8, 11],
                [6, 12],
            ],
            60,
            600,
            360,
        ),
        (6, [[1, 2], [1, 3], [2, 4], [3, 5], [5, 4], [4, 6]], 3, 100, 12),
    ],
)
def test_secondMinimum(n, edges, time, change, expected):
    s = Solution()
    assert s.secondMinimum(n, edges, time, change) == expected
