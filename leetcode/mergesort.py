import random


def mergesort(array):
    """Divide and conquer."""
    n = len(array)
    if n <= 1:
        return array

    # divide
    mid = n // 2
    left = mergesort(array[:mid])
    right = mergesort(array[mid:])

    # conquer (combine)
    i, j = 0, 0
    combi = list()
    while i < mid and j < n - mid:
        if left[i] < right[j]:
            combi.append(left[i])
            i += 1
        else:
            combi.append(right[j])
            j += 1
    # add remainder
    if i == mid:
        combi.extend(right[j:])
    else:
        combi.extend(left[i:])
    return combi


if __name__ == "__main__":
    n = 100
    max_ = int(1e7)
    random_ints = [random.randint(0, max_) for _ in range(n)]
    print(mergesort(random_ints))
