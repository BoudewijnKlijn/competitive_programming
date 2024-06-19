import re
from itertools import count, product

import numpy as np

EPS = 1e-10


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


def part2(content, alpha_rock=0.5, alpha_hail=0.5, R0=(1, 1, 1), Rv=(1, 1, 1)):
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

    H = np.array(hailstones)
    H0 = H[:, :3]
    Hv = H[:, 3:]

    max_iter = 1_000
    total_iterations = 0
    Ht = np.zeros(shape=(H0.shape[0], 1))
    losses = None

    Hp = H0 + Hv * Ht

    for i in count(1, step=1):
        if i > max_iter:
            print("EXIT: max iter", i)
            break

        # for each hailstone point determine at which time the rock line is the closest
        # then use that time to determine the point on the rock line
        # then switch roles, and find the optimal t for the hailstone line to be closest to the
        # rock line. store that time for the next iteration
        t_rock = get_optimal_t(Hp, R0, Rv)
        # loss = calc_loss(Hp, R0, Rv, t_rock)
        # print(f"loss before moving hailstones {loss}")
        Rp = R0 + t_rock * Rv
        new_Ht = np.zeros_like(Ht)
        for j in range(new_Ht.shape[0]):
            new_Ht[j] = get_optimal_t(
                Rp[j : j + 1, :], H0[j : j + 1, :], Hv[j : j + 1, :]
            )
        new_Ht = np.maximum(0, (1 - alpha_hail) * Ht + alpha_hail * new_Ht)

        if np.allclose(Ht, new_Ht, rtol=EPS):
            print("EXIT: converged times", i)
            break

        # update hailstone times
        Ht = new_Ht

        Hp = H0 + Hv * Ht

        # find the best rock line
        R0, Rv, losses, total_iterations = determine_best_line(
            Hp,
            R0,
            Rv,
            # losses=losses,
            losses=None,  # None for speedup
            alpha_rock=alpha_rock,
            total_iterations=total_iterations,
        )

    # round times to integer values (not sure if correct for real data)
    ts_hail = np.round(Ht).astype(int)
    # print(ts_hail)
    Hp = H0 + Hv * ts_hail

    rock_params = get_rock_parameters(Hp, ts_hail)
    print(rock_params)

    return R0, Rv, rock_params, losses[-1], total_iterations


def get_rock_parameters(Hp, Ht):
    """If loss is ~zero, the rock line can be determined from two hailstone lines with different
    times."""
    n = Hp.shape[0]
    for i in range(n):
        for j in range(n):
            if i == j or Ht[i] == Ht[j]:
                continue

            delta_Ht = Ht[i, :] - Ht[j, :]
            delta_Hp = Hp[i, :] - Hp[j, :]
            Rv = delta_Hp / delta_Ht
            R0 = Hp[i, :] - Ht[i] * Rv

            return R0, Rv


def get_optimal_t(point, line_0, line_v):
    """(dx * (x - x0) + dy * (y - y0) + dz * (z - z0)) / (dx**2 + dy**2 + dz**2)"""
    assert point.shape[1] == 3, "Wrong dimensions for point"
    assert line_0.shape == (1, 3), "Wrong dimensions for line_0"
    assert line_v.shape == (1, 3), "Wrong dimensions for line_v"
    return (point - line_0) @ line_v.T / np.sum(line_v**2, axis=1, keepdims=True)


def calc_loss(point, line_0, line_v, t):
    return np.mean((point - (line_0 + t * line_v)) ** 2)


def determine_best_line(
    Hp, R0, Rv, max_iter=1_000, losses=None, alpha_rock=0.8, total_iterations=0
):
    """Determine the best line that is closest to all points in 3D space."""
    if losses is None:
        losses = list()

    for epoch in count(1, step=1):
        if epoch > max_iter:
            # print("best line max iter reached", epoch)
            break

        t = get_optimal_t(Hp, R0, Rv)
        loss = calc_loss(Hp, R0, Rv, t)

        dR0 = 2 * np.mean(R0 - Hp + Rv * t, axis=0)
        dRv = 2 * np.mean(((R0 - Hp) * t + Rv), axis=0)

        # update parameters
        R0 -= alpha_rock * dR0
        Rv -= alpha_rock * dRv

        losses.append(loss)

        if losses[-1] < EPS:
            # print(f"converged loss {losses[-1]}, absolute", epoch)
            break

        if len(losses) > 1 and np.isclose(losses[-2], losses[-1], rtol=EPS):
            # print(f"converged loss {losses[-2]} {losses[-1]}, , relative", epoch)
            break

    # print("loss best line", losses[-1])
    # print("parameters", R0, Rv)

    total_iterations += epoch

    return R0, Rv, losses, total_iterations


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

    # alphas = np.linspace(0.9, 0.99, 9)
    # results = list()
    # for alpha in alphas:
    #     print(alpha)
    #     result = part2(
    #         SAMPLE,
    #         alpha_rock=0.6,
    #         alpha_hail=alpha,
    #     )
    #     results.append(result)
    #
    # for alpha, result in zip(alphas, results):
    #     print(alpha, result)

    initial0 = (-100, 100)
    initialv = (-100, 100)
    # initial0 = [2.65E+14, -2.65E+14]
    # initialv = [2.65E+14, -2.65E+14]
    i = 0
    smallest_loss = 1e10
    for x0, y0, z0 in product(initial0, repeat=3):
        R0 = np.array([x0, y0, z0], dtype=np.float64).reshape(1, 3)
        for xv, yv, zv in product(initialv, repeat=3):
            print(i, x0, y0, z0, "+", xv, yv, zv)
            Rv = np.array([xv, yv, zv], dtype=np.float64).reshape(1, 3)
            R0, Rv, rock_params, loss, total_iterations = part2(
                SAMPLE, alpha_rock=0.5, alpha_hail=0.9, R0=R0, Rv=Rv
            )
            # R0, Rv, rock_params, loss, total_iterations = part2(
            #     CONTENT, alpha_rock=0.5, alpha_hail=0.9, R0=R0, Rv=Rv
            # )
            if loss < smallest_loss:
                smallest_loss = loss
            print(R0, Rv, rock_params, f"{loss=}", total_iterations)
            i += 1

    print(smallest_loss)
    # print(part2(SAMPLE, alpha_rock=0.5, alpha_hail=0.9))
    # print(part2(CONTENT, alpha_rock=0.5, alpha_hail=0.9))
