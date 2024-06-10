import re
from itertools import product

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.preprocessing import StandardScaler
from sympy import factorint
from sklearn.linear_model import LinearRegression

pd.set_option("display.max_columns", None)


def part1(content, bounds=(7, 27)):
    hailstones = list()
    for line in content.split("\n"):
        data = list(map(int, re.findall(r"-?\d+", line)))
        hailstones.append(data)

    ans = 0

    for i, hailstone_1 in enumerate(hailstones):
        x10, y10, _, dx1dt, dy1dt, _ = hailstone_1
        for hailstone_2 in hailstones[i + 1 :]:
            x20, y20, _, dx2dt, dy2dt, _ = hailstone_2

            try:
                y = ((x20 - x10) + (y10 * dx1dt / dy1dt - y20 * dx2dt / dy2dt)) / (
                    dx1dt / dy1dt - dx2dt / dy2dt
                )
                x = (y - y10) / dy1dt * dx1dt + x10
                t1 = (x - x10) / dx1dt
                t2 = (x - x20) / dx2dt
            except ZeroDivisionError:
                # parallel
                continue

            if t1 < 0 or t2 < 0:
                # paths crossed in the past
                continue

            if not (bounds[0] <= x <= bounds[1] and bounds[0] <= y <= bounds[1]):
                # outside test area
                continue

            # print(hailstone_1, hailstone_2, x, y, t1, t2)
            ans += 1

    return ans


def part2(content):
    """We are looking for a straight line that passes all other 3D lines.
    To start, I ignore the time, I just try to find a line that goes through all other lines.
    Once I found that line I will derive the starting point and velocities, such that the line perfectly collides.
    To find the line that intersects all others:
    - Some point ABC intersects with a hail line if the following holds:
        A/vx - x0/vx = B/vy - y0/vy = C/vz - z0/vz
    - Then I just set A to some value and solve for B and C.
    - If not all B and C points are on a line, I have to adjust the A value.

    Loss doesn't become zero, so approach doesn't work.
    """
    hailstones = list()
    for line in content.split("\n"):
        data = list(map(int, re.findall(r"-?\d+", line)))
        hailstones.append(data)



    model = LinearRegression()

    # find the line that intersects all other lines
    losses = list()
    # as_ = list(range(10, 20))
    bs = np.linspace(18, 20, 100)
    for b in bs:

        as_ = list()
        # bs = list()
        cs = list()
        for i, hailstone in enumerate(hailstones):
            x0, y0, z0, vx, vy, vz = hailstone

            # b = y0 + vy * (a - x0) / vx
            # c = z0 + vz * (a - x0) / vx
            a = x0 + vx * (b - y0) / vy
            c = z0 + vz * (b - y0) / vy

            as_.append(a)
            # bs.append(b)
            cs.append(c)

            # print(a, b, c)

        # break
        model.fit(np.array(as_).reshape(-1, 1), np.array(cs).reshape(-1, 1))
        pred = model.predict(np.array(as_).reshape(-1, 1))
        loss = np.mean((np.array(cs) - pred) ** 2)
        losses.append(loss)
        print(b, loss)
    plt.plot(bs, losses)
    plt.show()




if __name__ == "__main__":
    SAMPLE = """19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3"""

    assert part1(SAMPLE) == 2

    with open("day24.txt", "r") as f:
        CONTENT = f.read().strip()

    BOUNDS = (200000000000000, 400000000000000)

    # print(part1(CONTENT, bounds=BOUNDS))

    # assert part2(SAMPLE) == 47

    print(part2(SAMPLE))

    # analysis(SAMPLE)
    # print(part2(CONTENT))
