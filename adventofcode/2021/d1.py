from typing import Iterable, List, Union


def load_data(filename) -> List[int]:
    with open(filename, 'r') as f:
        return list(map(int, f.read().split()))


def count_increasing(depths: Iterable) -> int:
    prev = None
    cnt_ = 0
    for depth in depths:
        if prev is None:
            pass
        elif depth > prev:
            cnt_ += 1
        prev = depth
    return cnt_


def sliding_sum(depths: List[Union[int]], window_size: int) -> Iterable[Union[int]]:
    assert window > 0
    return (sum(depths[i:i + window_size]) for i in range(len(depths) - window_size + 1))


if __name__ == '__main__':
    input_file = 'day1.txt'
    data = load_data(input_file)

    p1 = count_increasing(data)
    print(f'Part 1: {p1}')

    window = 3
    p2 = count_increasing(
        sliding_sum(data, window)
    )
    print(f'Part 2: {p2}')
