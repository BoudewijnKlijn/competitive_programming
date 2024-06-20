import re
from itertools import count, product

import numpy as np

np.set_printoptions(precision=20)


EPS = 1e-1


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


def part2(content, alpha_rock=0.5, alpha_hail=0.5, R0=None, Rv=None, Ht=None):
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
    n = H.shape[0]
    H0 = H[:, :3]
    Hv = H[:, 3:]

    # rnd_ids = None
    # if H.shape[0] > 5:
    #     rnd_ids = np.random.randint(0, H.shape[0], size=(5,))
    #     print(f"{rnd_ids=}")
    #     H0 = H[rnd_ids, :3]
    #     Hv = H[rnd_ids, 3:]

    batch_size = 5
    if n > 5:
        batch_size = 6

    n_batches = n // batch_size

    max_epoch = 100_000
    if Ht is None:
        Ht = np.zeros(shape=(H0.shape[0], 1))
    losses = list()

    Hp = H0 + Hv * Ht

    # Adam parameters
    use_adam = False
    b1 = 0.9
    b2 = 0.999
    eps = 1E-8
    m = 0
    v = 0
    delta = None

    stop = False
    for epoch in count(1, step=1):
        if stop:
            print("stop")
            break

        if stop or epoch > max_epoch:
            print("EXIT: max iter", epoch)
            break

        for batch_i in range(n_batches):
            # for each hailstone point determine at which time the rock line is the closest
            # then use that time to determine the point on the rock line
            # then switch roles, and find the optimal t for the hailstone line to be closest to the
            # rock line. store that time for the next iteration
            bb = batch_i * batch_size
            be = (batch_i + 1) * batch_size

            # t_rock = get_optimal_t(Hp, R0, Rv)
            # # print(f"{t_rock=}")
            # # loss = calc_loss(Hp, R0, Rv, t_rock)
            # # print(f"loss before moving hailstones {loss}")
            # Rp = R0 + t_rock * Rv
            # new_Ht = Ht.copy()
            # for j in range(bb, be):
            #     new_Ht[j] = get_optimal_t(
            #         Rp[j : j + 1, :], H0[j : j + 1, :], Hv[j : j + 1, :]
            #     )
            # new_Ht = np.maximum(0, (1 - alpha_hail) * Ht + alpha_hail * new_Ht)

            # if np.allclose(Ht, new_Ht, rtol=EPS):
            #     print("EXIT: converged times", epoch)
            #     stop = True
            #     break

            # # update hailstone times
            # Ht = new_Ht

            Hp = H0 + Hv * Ht

            # find the best rock line
            # R0, Rv, losses, total_iterations = determine_best_line(
            #     Hp,
            #     R0,
            #     Rv,
            #     max_iter=max_iter_rock,
            #     # losses=losses,
            #     losses=None,  # None for speedup
            #     alpha_rock=alpha_rock,
            #     total_iterations=total_iterations,
            # )

            t_rock = get_optimal_t(Hp[bb:be], R0, Rv)
            loss = calc_loss(Hp[bb:be], R0, Rv, t_rock)

            dR0 = 2 * np.mean(R0 - Hp[bb:be] + Rv * t_rock, axis=0)
            dRv = 2 * np.mean(((R0 - Hp[bb:be]) * t_rock + Rv), axis=0)
            # print(dR0, dRv)

            if use_adam:
                # update parameters: Adam
                g = np.hstack((dR0, dRv))
                m = b1 * m + (1 - b1) * g
                v = b2 * v + (1 - b2) * g ** 2
                m_hat = m / (1 - b1 ** epoch)
                v_hat = v / (1 - b2 ** epoch)
                delta = alpha_rock * m_hat / (v_hat ** 0.5 + eps)
                R0 -= delta[:3]
                Rv -= delta[3:]
                # print(delta)
            else:
                # update parameters: SGD
                R0 -= alpha_rock * dR0
                Rv -= alpha_rock * dRv

            losses.append(loss)

            if losses[-1] < EPS:
                print(f"EXIT: converged loss {losses[-1]}, absolute", epoch)
                stop = True
                break

            # if len(losses) > 1 and np.isclose(losses[-2], losses[-1], rtol=EPS):
            #     print(f"EXIT: converged loss {losses[-2]} {losses[-1]}, relative", epoch)
            #     stop = True
            #     break

        if epoch % 100 == 0:
            print(f"{epoch=}, loss={np.mean(losses[-n_batches:])}, {R0=}, {Rv=}, ")
                  # f"{Ht=}")

    # round times to integer values (not sure if correct for real data)
    ts_hail = np.round(Ht).astype(np.int64)
    # print(ts_hail)
    Hp = H0 + Hv * ts_hail

    rock_params = get_rock_parameters(Hp, ts_hail)
    print(f"{rock_params=}")
    t_rock = get_optimal_t(Hp, *rock_params)
    loss = calc_loss(Hp, *rock_params, t_rock)
    print("loss", loss)
    # print("ans=", np.sum(rock_params)) # fout: enkel r0, niet ook rv

    r0, rv = rock_params
    print("ans=", np.sum(r0))
    for h, ht, rt in zip(Hp, Ht, t_rock):
        print(h, r0 + rv * rt)

        l = h - (r0 + rv * ht)
        print("loss", l, ht, rt, ht - rt)


    return R0, Rv, rock_params, losses[-1], epoch


def get_rock_parameters(Hp, Ht):
    """If loss is ~zero, the rock line can be determined from two hailstone lines with different
    times."""
    n = Hp.shape[0]
    for i in range(n):
        for j in range(i+1, n):
            if i == j or Ht[i] == Ht[j]:
                continue

            delta_Ht = Ht[i, :] - Ht[j, :]
            delta_Hp = Hp[i, :] - Hp[j, :]
            Rv = delta_Hp / delta_Ht
            R0 = Hp[i, :] - Ht[i] * Rv
            # print(f"{R0=}, {Rv=}")

            return R0.reshape(1, 3), Rv.reshape(1, 3)


def get_optimal_t(point, line_0, line_v):
    """(dx * (x - x0) + dy * (y - y0) + dz * (z - z0)) / (dx**2 + dy**2 + dz**2)"""
    assert point.shape[1] == 3, f"Wrong dimensions for point, {point.shape}"
    assert line_0.shape == (1, 3), f"Wrong dimensions for line_0, {line_0.shape}"
    assert line_v.shape == (1, 3), f"Wrong dimensions for line_v, {line_v.shape}"
    return (point - line_0) @ line_v.T / np.sum(line_v**2, axis=1, keepdims=True)


def calc_loss(point, line_0, line_v, t):
    return np.mean((point - (line_0 + t * line_v)) ** 2)


# def determine_best_line(
#     Hp, R0, Rv, max_iter=1_000, losses=None, alpha_rock=0.8, total_iterations=0
# ):
#     """Determine the best line that is closest to all points in 3D space."""
#     if losses is None:
#         losses = list()
#
#     for epoch in count(1, step=1):
#         if epoch > max_iter:
#             epoch -= 1
#             # print("best line max iter reached", epoch)
#             break
#
#         t = get_optimal_t(Hp, R0, Rv)
#         loss = calc_loss(Hp, R0, Rv, t)
#
#         dR0 = 2 * np.mean(R0 - Hp + Rv * t, axis=0)
#         dRv = 2 * np.mean(((R0 - Hp) * t + Rv), axis=0)
#
#         # update parameters
#         R0 -= alpha_rock * dR0
#         Rv -= alpha_rock * dRv
#
#         losses.append(loss)
#
#         if losses[-1] < EPS:
#             # print(f"converged loss {losses[-1]}, absolute", epoch)
#             break
#
#         if len(losses) > 1 and np.isclose(losses[-2], losses[-1], rtol=EPS):
#             # print(f"converged loss {losses[-2]} {losses[-1]}, , relative", epoch)
#             break
#
#     # print("loss best line", losses[-1])
#     # print("parameters", R0, Rv)
#
#     total_iterations += epoch
#
#     return R0, Rv, losses, total_iterations


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

    # # varying alphas (hail and rock)
    # c = 1e1
    # R0 = np.array([c, c, c], dtype=np.float64).reshape(1, 3)
    # Rv = np.array([c, c, c], dtype=np.float64).reshape(1, 3)
    # alphas = np.linspace(0.1, 0.9, 9)
    # results = list()
    # for alpha in alphas:
    #     print(alpha)
    #     result = part2(
    #         SAMPLE,
    #         alpha_rock=0.5,
    #         alpha_hail=0.6,
    #         R0=R0.copy(),
    #         Rv=Rv.copy(),
    #     )
    #     results.append(result)
    #
    # for alpha, result in zip(alphas, results):
    #     print(alpha, result)

    # # varying initial states
    # c = 1e2
    # initial0 = (-c, c)
    # initialv = (-c, c)
    # i = 0
    # smallest_loss = 1e30
    # for x0, y0, z0 in product(initial0, repeat=3):
    #     R0 = np.array([x0, y0, z0], dtype=np.float64).reshape(1, 3)
    #     for xv, yv, zv in product(initialv, repeat=3):
    #         print(i, x0, y0, z0, "+", xv, yv, zv)
    #         Rv = np.array([xv, yv, zv], dtype=np.float64).reshape(1, 3)
    #         # R0, Rv, rock_params, loss, total_iterations = part2(
    #         #     SAMPLE, alpha_rock=0.6, alpha_hail=0.8, R0=R0.copy(), Rv=Rv.copy()
    #         # )
    #         R0, Rv, rock_params, loss, total_iterations = part2(
    #             CONTENT, alpha_rock=0.6, alpha_hail=0.8, R0=R0.copy(), Rv=Rv.copy()
    #         )
    #         if loss < smallest_loss:
    #             smallest_loss = loss
    #         print(R0, Rv, rock_params, f"{loss=}", total_iterations)
    #         i += 1
    # print(smallest_loss)

    # # keep running until we find really low loss.
    # # identical initial states, but 5 random hail trajectories
    # c = 1e2
    # R0 = np.array([c, c, c], dtype=np.float64).reshape(1, 3)
    # Rv = np.array([c, c, c], dtype=np.float64).reshape(1, 3)
    # i = 0
    # smallest_loss = 1e30
    # best = None
    # for i in count(1):
    #     result = part2(
    #         CONTENT, alpha_rock=0.001, alpha_hail=0.001, R0=R0.copy(), Rv=Rv.copy()
    #     )
    #     print(result)
    #     if result[3] < smallest_loss:
    #         smallest_loss = result[3]
    #         best = result
    #     if i % 20 == 0:
    #         print(i, "best", smallest_loss, best)

    # c = 1e1
    # R0 = np.array([c, c, c], dtype=np.float64).reshape(1, 3)
    # Rv = np.array([c, c, c], dtype=np.float64).reshape(1, 3)
    # R0 = np.array([[2.71714385e+14, 2.70787818e+14, 2.76385340e+14]])
    # Rv = np.array([[4.08753367e+13, -1.31053915e+14, -4.63534746e+12]])

    # print(part2(SAMPLE, alpha_rock=0.1, alpha_hail=0.2, R0=R0.copy(), Rv=Rv.copy()))

    # R0 = np.array([[2.6528635672420647e+14, 2.9139726992287019e+14,
    #                 2.7711429175188378e+14]])
    # Rv = np.array([[2.967344187588408e+13, -9.513856106597925e+13,
    #                 -3.365029491079811e+12]])
    R0 = np.array([[3.24764920956014e+14, 1.00697955736353e+14, 2.70369299931782e+14]])
    Rv = np.array(
        [[-97., 311., 11.]])
    Ht = np.array([[5.205578030920e+11],
       [9.910704793130e+11],
       [6.262810249240e+11],
       [5.922142817450e+11],
       [7.779163024730e+11],
       [6.018818340700e+11],
       [6.397399097390e+11],
       [5.280873917720e+11],
       [6.185945631030e+11],
       [7.714486241250e+11],
       [3.251326966540e+11],
       [3.318409176630e+11],
       [5.568107072140e+11],
       [4.141282200450e+11],
       [3.236900252340e+11],
       [7.199556294600e+10],
       [7.294746621040e+11],
       [9.905445714980e+11],
       [8.041030042360e+11],
       [4.349944336400e+11],
       [7.881943176350e+11],
       [6.141496818880e+11],
       [7.183719045590e+11],
       [8.405502453000e+10],
       [5.677126329830e+11],
       [2.339265388190e+11],
       [3.332806149590e+11],
       [5.367856972270e+11],
       [5.613333815500e+10],
       [8.303843018900e+10],
       [6.641241787300e+11],
       [7.556784173600e+11],
       [5.979727087630e+11],
       [4.019394213340e+11],
       [8.698372551520e+11],
       [9.052813036810e+11],
       [5.352220950900e+11],
       [9.567129294720e+11],
       [8.329746804460e+11],
       [2.816533138370e+11],
       [6.965575651910e+11],
       [9.255722552720e+11],
       [8.316717723660e+11],
       [1.779981090330e+11],
       [1.607893852130e+11],
       [3.211825389780e+11],
       [1.236279620160e+11],
       [3.816833739870e+11],
       [1.221626492990e+11],
       [1.699445402290e+11],
       [1.034713998130e+11],
       [9.216149988080e+11],
       [4.130991444270e+11],
       [4.865402096490e+11],
       [2.729839570970e+11],
       [7.210719895360e+11],
       [6.311020382860e+11],
       [5.920329169090e+11],
       [5.622755229770e+11],
       [8.108008099750e+11],
       [8.645647310390e+11],
       [1.705454730870e+11],
       [2.478579077860e+11],
       [2.188990660000e+11],
       [9.142092997650e+11],
       [7.611341195020e+11],
       [1.019318739640e+12],
       [2.947681059140e+11],
       [1.815371890630e+11],
       [5.856788662500e+10],
       [1.018771901100e+11],
       [2.649132412750e+11],
       [6.903394803430e+11],
       [1.024608928293e+12],
       [7.864719484350e+11],
       [8.447291645750e+11],
       [6.773077147960e+11],
       [5.336045650500e+11],
       [1.020993163441e+12],
       [5.108561779570e+11],
       [3.657075995320e+11],
       [2.141221481980e+11],
       [8.138836818820e+11],
       [4.131994262610e+11],
       [2.475707467640e+11],
       [2.188206893690e+11],
       [5.589725356810e+11],
       [5.496646929570e+11],
       [1.049855506260e+11],
       [6.302469082190e+11],
       [6.244247287450e+11],
       [7.733341991680e+11],
       [1.531844677750e+11],
       [7.404296572200e+10],
       [7.343998447240e+11],
       [6.496912877870e+11],
       [5.201848898820e+11],
       [1.424629671830e+11],
       [8.454613251830e+11],
       [4.886214054760e+11],
       [8.146076268470e+11],
       [8.192751712300e+11],
       [8.382272570290e+11],
       [5.538015774790e+11],
       [3.422376042620e+11],
       [6.626647688960e+11],
       [1.059714995600e+11],
       [8.146014059810e+11],
       [3.779534039040e+11],
       [9.832944929060e+11],
       [8.584563712770e+11],
       [8.546886379280e+11],
       [3.704954976310e+11],
       [5.804387851150e+11],
       [8.173105202760e+11],
       [1.538236878200e+11],
       [9.991383590440e+11],
       [4.160756389900e+11],
       [8.239404191300e+11],
       [9.864910047960e+11],
       [7.078479195260e+11],
       [4.289232067140e+11],
       [9.169138652810e+11],
       [9.368635100620e+11],
       [9.154353626010e+11],
       [1.912460909270e+11],
       [4.093126059190e+11],
       [5.406122609120e+11],
       [8.823174950240e+11],
       [9.324855453350e+11],
       [5.099963213980e+11],
       [4.575729953330e+11],
       [9.668890140020e+11],
       [4.103272354960e+11],
       [9.910215721740e+11],
       [8.465325032070e+11],
       [5.797457970970e+11],
       [1.686278294410e+11],
       [5.885817294060e+11],
       [8.038352108430e+11],
       [3.176554282250e+11],
       [9.706913093740e+11],
       [1.780790620160e+11],
       [6.643259477130e+11],
       [2.462643478960e+11],
       [1.027994105251e+12],
       [2.127158910070e+11],
       [1.016184298245e+12],
       [2.029555590020e+11],
       [7.627325074480e+11],
       [1.023389795012e+12],
       [7.093975108410e+11],
       [6.948997059270e+11],
       [2.831796469110e+11],
       [1.541040131840e+11],
       [6.391103530440e+11],
       [3.886156449390e+11],
       [2.540772621360e+11],
       [7.187702823860e+11],
       [2.435581329690e+11],
       [4.018295506270e+11],
       [1.705745793910e+11],
       [9.470612664220e+11],
       [6.819858860280e+11],
       [2.180864751380e+11],
       [3.066341595240e+11],
       [8.314821966660e+11],
       [9.540441050740e+11],
       [6.507969243900e+10],
       [4.951286687100e+11],
       [9.431180632140e+11],
       [9.451057152200e+11],
       [6.870007435900e+11],
       [4.430127742810e+11],
       [9.559982132060e+11],
       [1.048827518070e+11],
       [9.627198451770e+11],
       [9.703075318820e+11],
       [8.081403487970e+11],
       [4.555805720000e+11],
       [1.973485864280e+11],
       [4.622591889590e+11],
       [6.970746365870e+11],
       [8.936092428180e+11],
       [4.452224116700e+11],
       [1.376934375750e+11],
       [8.660761849890e+11],
       [1.333110300210e+11],
       [2.513562253860e+11],
       [7.417035935610e+11],
       [7.787782215630e+11],
       [3.641082370940e+11],
       [2.234699450530e+11],
       [5.443077099410e+11],
       [4.976834024060e+11],
       [1.050284143010e+11],
       [9.741461560560e+11],
       [1.030274650562e+12],
       [2.322079293820e+11],
       [6.134772430710e+11],
       [5.728167747490e+11],
       [6.914147816360e+11],
       [1.406969838960e+11],
       [7.027369002670e+11],
       [8.324820289860e+11],
       [4.272927534070e+11],
       [1.031127206110e+11],
       [2.509114162710e+11],
       [1.408217731390e+11],
       [9.399504513660e+11],
       [6.760054526130e+11],
       [5.851232222200e+10],
       [6.658767031440e+11],
       [3.554453830170e+11],
       [5.800952009750e+11],
       [5.771210461790e+11],
       [1.017265405088e+12],
       [9.756136676720e+11],
       [7.559944497880e+11],
       [8.142967669420e+11],
       [1.599903269920e+11],
       [6.321981869530e+11],
       [3.352516256340e+11],
       [4.361806487750e+11],
       [2.620063707700e+11],
       [7.732499506370e+11],
       [3.000129746960e+11],
       [2.177922342720e+11],
       [8.115788401370e+11],
       [4.072972873630e+11],
       [7.573191253370e+11],
       [3.920717522640e+11],
       [7.394645747150e+11],
       [5.891249643000e+11],
       [5.552173192200e+11],
       [6.405636434180e+11],
       [2.008313073220e+11],
       [5.587155438910e+11],
       [2.964475151610e+11],
       [2.848077514130e+11],
       [7.586359873160e+11],
       [9.584947256170e+11],
       [2.510897763230e+11],
       [8.684971858390e+11],
       [1.001059393094e+12],
       [5.689331223470e+11],
       [6.202344057980e+11],
       [4.824618483310e+11],
       [9.017911852160e+11],
       [4.544669032130e+11],
       [7.390669062870e+11],
       [7.910632868010e+11],
       [6.969421021060e+11],
       [8.207543144510e+11],
       [7.644315342880e+11],
       [4.952582352480e+11],
       [5.981508804540e+11],
       [4.683224483780e+11],
       [5.079332343720e+11],
       [6.484399998830e+11],
       [8.242555436220e+11],
       [4.934683128520e+11],
       [1.139206487680e+11],
       [7.106410609700e+10],
       [5.486939037050e+11],
       [5.884223445690e+11],
       [8.917882423400e+11],
       [9.224907003300e+10],
       [6.228696975550e+11],
       [8.273993277160e+11],
       [4.190978607080e+11],
       [1.020848944333e+12],
       [6.733902885080e+11],
       [1.033307099369e+12],
       [3.010208518830e+11],
       [1.404915207940e+11],
       [4.056050990350e+11],
       [1.023385891967e+12],
       [1.451938908530e+11],
       [4.130400688930e+11],
       [9.749437216040e+11],
       [3.358098461120e+11],
       [3.238374925000e+11],
       [7.920096532020e+11],
       [9.066319614780e+11],
       [3.006443130080e+11],
       [6.746553707220e+11],
       [3.332634710880e+11],
       [1.764640728180e+11],
       [4.634700664660e+11],
       [2.095896897030e+11],
       [4.716247550560e+11],
       [7.309865640200e+10],
       [5.724593874780e+11],
       [4.335259802040e+11],
       [3.842839589320e+11],
       [1.166183595380e+11],
       [5.522052816020e+11],
       [1.002240180756e+12],
       [8.085580193720e+11]])
    print(part2(CONTENT, alpha_rock=0.01, alpha_hail=0.1, R0=R0.copy(), Rv=Rv.copy(), Ht=Ht.copy()))

    # too high: 695832176624374
    # 695832176624149: correct