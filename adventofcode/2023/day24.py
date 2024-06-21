import re
from itertools import count

import numpy as np

np.set_printoptions(precision=15)

LOSS_GOAL = 1e-2


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


def part2(content, alpha_rock, alpha_hail, R0, Rv):
    """We are searching a straight line (rock) that collides with all other 3D lines (hail).
    Times of rock and hail should match perfectly to collide, but I assume that only one rock line
    exists that intersects all hailstone lines. Hence, timing is somewhat irrelevant.
    Time is only need to find the rock starting rock point, the answer.

    The approach has a few steps (similar to k-means):
    1. initialize all hailstone times at 0 and determine hailstone points
    2. find the rock line that has the minimal distance to all hailstone points
    3. adjust hailstone times to move the hailstones along their trajectory such that they move
    closer to the rock line
    4. repeat from step 2, until convergence

    Most helpful:
    - using batches. The optimization gets stuck in local optimum when all 300 hailstones are used
    at once. We only need a few hailstones to determine the rock line.

    Tried (and didn't work):
    - only using small number of _random_ hailstones, in the hope the initialization would be good
    - Adam optimzer: slower than SGD. Parameters are large and Adam steps very small.
    Scaling the inputs didn't help.
    - torch: slower than numpy
    - different R0 and Rv initializations
    - different learning rates
    """
    hailstones = list()
    for line in content.split("\n"):
        data = list(map(int, re.findall(r"-?\d+", line)))
        hailstones.append(data)

    H = np.array(hailstones)
    n = H.shape[0]
    H0 = H[:, :3]
    Hv = H[:, 3:]
    Ht = np.zeros(shape=(H0.shape[0], 1), dtype=np.float64)
    Hp = H0 + Hv * Ht

    batch_size = 5
    if n > 5:
        batch_size = 6
    n_batches = n // batch_size

    max_epoch = 10_000
    losses = list()
    for epoch in count(1, step=1):

        if epoch > max_epoch:
            print(f"EXIT: Max epochs.")
            break

        if epoch > 1 and np.mean(losses[-n_batches:]) < LOSS_GOAL:
            print(f"EXIT: Loss converged.")
            break

        for batch_i in range(n_batches):
            bb = batch_i * batch_size  # begin id batch
            be = (batch_i + 1) * batch_size  # end id batch

            # for each hailstone point determine at which time the rock line is the closest
            # then use that time to determine the point on the rock line
            # then switch roles, and find the optimal t for the hailstone line to be closest to the
            # rock line. store that time for the next iteration
            t_rock = get_optimal_t(Hp, R0, Rv)
            Rp = R0 + t_rock * Rv
            new_Ht = Ht.copy()
            for j in range(bb, be):
                new_Ht[j] = get_optimal_t(
                    Rp[j : j + 1, :], H0[j : j + 1, :], Hv[j : j + 1, :]
                )
            Ht = np.maximum(0, (1 - alpha_hail) * Ht + alpha_hail * new_Ht)
            Hp = H0 + Hv * Ht

            t_rock = get_optimal_t(Hp[bb:be], R0, Rv)
            loss = calc_loss(Hp[bb:be], R0, Rv, t_rock)
            losses.append(loss)

            # partial derivatives
            dR0 = 2 * np.mean(R0 - Hp[bb:be] + Rv * t_rock, axis=0)
            dRv = 2 * np.mean(((R0 - Hp[bb:be]) * t_rock + Rv), axis=0)

            # update parameters
            R0 -= alpha_rock * dR0
            Rv -= alpha_rock * dRv

        if epoch % 100 == 0:
            print(f"{epoch=}, loss={np.mean(losses[-n_batches:])}")

    # finetune hailstone times: round to integers
    int_times = np.round(Ht).astype(np.int64)
    Hp = H0 + Hv * int_times

    # finetune rock parameters
    R0, Rv = get_rock_parameters(Hp, int_times)
    loss = calc_loss(Hp, R0, Rv, int_times)
    ans = int(np.sum(R0))
    print(f"{R0=}, {Rv=}\n" f"{loss=}, {ans=}")

    return ans


def get_rock_parameters(Hp, Ht):
    """If loss is ~zero, the rock line can be determined from just two hailstone lines with
    different times."""
    n = Hp.shape[0]
    for i in range(n):
        for j in range(i + 1, n):
            if i == j or Ht[i] == Ht[j]:
                continue

            delta_Ht = Ht[i, :] - Ht[j, :]
            delta_Hp = Hp[i, :] - Hp[j, :]
            Rv = delta_Hp / delta_Ht
            R0 = Hp[i, :] - Ht[i] * Rv

            return R0.reshape(1, 3), Rv.reshape(1, 3)


def get_optimal_t(point, line_0, line_v):
    """(dx * (x - x0) + dy * (y - y0) + dz * (z - z0)) / (dx**2 + dy**2 + dz**2)"""
    assert point.shape[1] == 3, f"Wrong dimensions for point, {point.shape}"
    assert line_0.shape == (1, 3), f"Wrong dimensions for line_0, {line_0.shape}"
    assert line_v.shape == (1, 3), f"Wrong dimensions for line_v, {line_v.shape}"
    return (point - line_0) @ line_v.T / np.sum(line_v**2, axis=1, keepdims=True)


def calc_loss(point, line_0, line_v, t):
    return np.mean((point - (line_0 + t * line_v)) ** 2)


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

    print(part1(CONTENT, bounds=BOUNDS))

    c = 1
    R0 = np.array([c, c, c], dtype=np.float64).reshape(1, 3)
    Rv = np.array([c, c, c], dtype=np.float64).reshape(1, 3)

    assert (
        part2(SAMPLE, alpha_rock=0.5, alpha_hail=0.5, R0=R0.copy(), Rv=Rv.copy()) == 47
    )

    print(
        part2(CONTENT, alpha_rock=0.3, alpha_hail=0.3, R0=R0.copy(), Rv=Rv.copy())
    )  # 695832176624149
