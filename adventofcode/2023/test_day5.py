import pytest

from day5 import adjust_ranges


@pytest.mark.parametrize(
    "start1,range1,dest_range_start,start2,range2,expected",
    [
        (10, 10, 100, 5, 5, ([(10, 10)], [])),
        (10, 10, 100, 20, 5, ([(10, 10)], [])),
        (10, 10, 100, 5, 20, ([], [(105, 10)])),
        (10, 10, 100, 5, 10, ([(15, 5)], [(105, 5)])),
        (10, 10, 100, 11, 100, ([(10, 1)], [(100, 9)])),
        (10, 10, 100, 15, 10, ([(10, 5)], [(100, 5)])),
        (10, 10, 100, 15, 2, ([(10, 5), (17, 3)], [(100, 2)])),
    ],
)
def test_adjust(start1, range1, dest_range_start, start2, range2, expected):
    assert adjust_ranges(start1, range1, dest_range_start, start2, range2) == expected
