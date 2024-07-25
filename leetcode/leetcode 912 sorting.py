import timeit

import matplotlib.pyplot as plt


def bubblesort(nums):
    for j in range(len(nums)):
        swapped = False  # for early stopping
        for i in range(len(nums) - 1 - j):
            if nums[i] > nums[i + 1]:
                nums[i], nums[i + 1] = nums[i + 1], nums[i]
                swapped = True
        if not swapped:
            break
    return nums


def merge(left, right):
    arr = []
    while left and right:
        if left[0] < right[0]:
            arr.append(left.pop(0))
        else:
            arr.append(right.pop(0))
    if left:
        arr.extend(left)
    else:
        arr.extend(right)
    return arr


def mergesort(nums):
    n = len(nums)
    if n <= 1:
        return nums

    mid = n // 2
    left = mergesort(nums[:mid])
    right = mergesort(nums[mid:])

    return merge(left, right)


def insertionsort(nums):
    for pos in range(1, len(nums)):
        current = nums[pos]
        while pos > 0 and nums[pos - 1] > current:
            nums[pos] = nums[pos - 1]
            pos -= 1
        nums[pos] = current
    return nums


def binaryinsertionsort(nums):
    arr = [nums[0]]
    for i in range(1, len(nums)):
        left, right = 0, len(arr)
        while left < right:
            mid = (left + right) // 2
            if arr[mid] < nums[i]:
                left = mid + 1
            else:
                right = mid
        arr.insert(left, nums[i])
    return arr


# print(bubblesort(array.copy()))
# print(mergesort(array.copy()))
# print(insertionsort(array.copy()))
# print(binaryinsertionsort(array.copy()))

elements = [10, 100, 1000, 3000, 10000]
funcs = [bubblesort, mergesort, insertionsort, binaryinsertionsort]

for func in funcs:
    times = []
    for elem in elements:
        array = list(range(elem))
        array.reverse()

        t = timeit.timeit(f"{func.__name__}(array.copy())", globals=globals(), number=3)
        times.append(t)
    plt.plot(elements, times, label=func.__name__)
plt.legend()
plt.xscale("log")
plt.yscale("log")
plt.show()
