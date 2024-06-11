import re
from itertools import count

import numpy as np
from matplotlib import pyplot as plt


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


def part2(content, alpha_rock=0.5):
    """We are looking for a straight line (rock) that intersects all other 3D lines (hail).
    To start, I ignore the time, I just try to find a line that intersects all other lines.
    Thereafter, I will derive the starting point and velocities, such that rock perfectly collides with all hails.

    The approach has two stages (similar to k-means):
    1. pick a random starting point on all hail lines.
    2. find the rock line (trajectory) that has the minimal distance to all these points.
    3. move the starting points along the hail line such that they move closer to the rock line.
    Repeat from step 2.

    This approach has ideas from the previous two approaches, but should work better because:
    - the points remain in the hailstone trajectories, instead of solving for t in 3 dimensions separately.
    - all three dimensions are used instead of fixing one.
    """
    hailstones = list()
    for line in content.split("\n"):
        data = list(map(int, re.findall(r"-?\d+", line)))
        hailstones.append(data)

    max_iter = 10_000
    total_iterations = 0
    alpha_hail = 0.9
    ts_hail = [0] * len(hailstones)
    losses = None

    # rock trajectory parameters initial guess
    x0, y0, z0, dx, dy, dz = 1, 2, 3, 4, 5, 6
    x0, y0, z0, dx, dy, dz = 100, -100, -100, 1, 1, 1

    for i in count(0, step=1):
        if i >= max_iter:
            print("adjust time max iter reached", i)
            break

        points = calc_hailstone_points(hailstones, ts_hail)

        # find the best rock line
        x0, y0, z0, dx, dy, dz, losses, total_iterations = determine_best_line(
            points, initial_guess=(x0, y0, z0, dx, dy, dz),
            # losses=losses,
            losses=None,  # speedup
            alpha_rock=alpha_rock,
            total_iterations=total_iterations,
        )

        # for each hailstone point determine at which time the rock line is the closest
        # then use that time to determine the point on the rock line
        # then switch roles, and find the optimal t for the hailstone line to be closest to the rock line
        # store that time for the next iteration
        new_ts_hail = list()
        for hailstone, point, t_hail_old in zip(hailstones, points, ts_hail):
            t_rock = get_optimal_t(point, (x0, y0, z0, dx, dy, dz))
            rock_point = (x0 + t_rock * dx, y0 + t_rock * dy, z0 + t_rock * dz)
            t_hail = get_optimal_t(rock_point, hailstone)
            new_t_hail = max((1 - alpha_hail) * t_hail_old + alpha_hail * t_hail, 0)
            new_ts_hail.append(new_t_hail)

        if np.allclose(ts_hail, new_ts_hail, rtol=1e-10):
            print("converged times, relative", i)
            break

        # update hailstone times
        ts_hail = new_ts_hail

    # round times to integer values (not sure if correct for real data)
    ts_hail = [round(t) for t in ts_hail]
    print(ts_hail)
    print(calc_hailstone_points(hailstones, ts_hail))

    # plt.plot(losses)
    # plt.show()

    return x0, y0, z0, dx, dy, dz, losses[-1], total_iterations


def calc_hailstone_points(hailstones, ts_hail):
    # calculate the points on the hailstone lines
    points = list()
    for t_hail, hailstone in zip(ts_hail, hailstones):
        points.append(
            (
                hailstone[0] + t_hail * hailstone[3],
                hailstone[1] + t_hail * hailstone[4],
                hailstone[2] + t_hail * hailstone[5],
            )
        )
    return points


def get_optimal_t(point, line):
    x, y, z = point
    x0, y0, z0, dx, dy, dz = line
    return (dx * (x - x0) + dy * (y - y0) + dz * (z - z0)) / (dx**2 + dy**2 + dz**2)


def determine_best_line(points: list, initial_guess, max_iter=10_000, losses=None, alpha_rock=0.8,
                        total_iterations=0):
    """Determine the best line that is closest to all points in 3D space."""
    x0, y0, z0, dx, dy, dz = initial_guess

    n = len(points)
    # alpha_rock = 0.8  # todo seems very sensitive to alpha
    if losses is None:
        losses = list()
    for i in count(0, step=1):
        if i >= max_iter:
            print("best line max iter reached", i)
            break

        loss = 0
        dx0, dy0, dz0, ddx, ddy, ddz = 0, 0, 0, 0, 0, 0
        for x, y, z in points:
            t = get_optimal_t((x, y, z), (x0, y0, z0, dx, dy, dz))
            loss += (
                (x - (x0 + t * dx)) ** 2
                + (y - (y0 + t * dy)) ** 2
                + (z - (z0 + t * dz)) ** 2
            )

            # partial derivatives
            dx0 += 2 * (x0 - x + dx * t) / n
            dy0 += 2 * (y0 - y + dy * t) / n
            dz0 += 2 * (z0 - z + dz * t) / n
            ddx += 2 * ((x0 - x) * t + dx) / n
            ddy += 2 * ((y0 - y) * t + dy) / n
            ddz += 2 * ((z0 - z) * t + dz) / n

        if loss < 1e-10:
            print("converged loss, absolute", i)
            losses.append(loss)
            break

        if len(losses) > 0 and np.isclose(loss, losses[-1], rtol=1e-10):
            print("converged loss, relative", i)
            break
        losses.append(loss)

        # update parameters
        x0 -= alpha_rock * dx0
        y0 -= alpha_rock * dy0
        z0 -= alpha_rock * dz0
        dx -= alpha_rock * ddx
        dy -= alpha_rock * ddy
        dz -= alpha_rock * ddz

        # normalize velocity parameters (to prevent overflows)
        norm = np.linalg.norm([dx, dy, dz])
        dz /= norm
        dy /= norm
        dx /= norm

        # shift starting point closest to the origin
        t = get_optimal_t((0, 0, 0), (x0, y0, z0, dx, dy, dz))
        x0 += t * dx
        y0 += t * dy
        z0 += t * dz

        # print(x0, y0, z0, dx, dy, dz)

    print("loss best line", loss)
    print("parameters", x0, y0, z0, dx, dy, dz)

    total_iterations += i

    return x0, y0, z0, dx, dy, dz, losses, total_iterations


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

    # alphas = np.linspace(0.1, 0.6, 6)
    # results = list()
    # for alpha in alphas:
    #     print(alpha)
    #     result = part2(SAMPLE, alpha_rock=alpha)
    #     results.append(result)
    #
    # for alpha, result in zip(alphas, results):
    #     print(alpha, result, result[4]/result[5])

    # print(part2(SAMPLE))
    print(part2(CONTENT, alpha_rock=0.3))
