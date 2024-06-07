import re
from itertools import product

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.preprocessing import StandardScaler
from sympy import factorint

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
    hailstones = list()
    for line in content.split("\n"):
        data = list(map(int, re.findall(r"-?\d+", line)))
        hailstones.append(data)

    use_scaler = False

    df = pd.DataFrame(hailstones)
    scaler = StandardScaler()
    df_transformed = pd.DataFrame(scaler.fit_transform(df))

    # rock starting values
    xr0, yr0, zr0, dxrdt, dyrdt, dzrdt = 0, 0, 0, 0, 0, 0
    xr0, yr0, zr0, dxrdt, dyrdt, dzrdt = 24, 13, 10, -3, 1, 2
    # xr0, yr0, zr0, dxrdt, dyrdt, dzrdt = 23, 13, 10, -3, 1, 2

    x10, y10, z10, dx1dt, dy1dt, dz1dt = df.iloc[0].values

    txs = list()
    tys = list()
    losses = list()
    dxrdts = list()
    dyrdts = list()
    df0 = pd.DataFrame(columns=["xr0", "yr0", "zr0", "dxrdt", "dyrdt", "dzrdt", "loss"])

    for dxrdt, dyrdt in product(range(-3, 4), repeat=2):
        dxrdts.append(dxrdt)
        dyrdts.append(dyrdt)
        tx = (x10 - xr0) / (dxrdt - dx1dt) if (dxrdt - dx1dt) != 0 else np.nan
        ty = (y10 - yr0) / (dyrdt - dy1dt) if (dyrdt - dy1dt) != 0 else np.nan

        df0 = df0._append(
            {
                "xr0": xr0,
                "yr0": yr0,
                "zr0": zr0,
                "dxrdt": dxrdt,
                "dyrdt": dyrdt,
                "dzrdt": dzrdt,
                "loss": (tx - ty) ** 2,
            },
            ignore_index=True,
        )

        loss = (tx - ty) ** 2
        print(dxrdt, dyrdt, tx, ty, loss)
        txs.append(tx)
        tys.append(ty)
        losses.append(loss)

    # plt.plot(dxrdts, losses, label="tx")
    # plt.show()
    # plt.plot(dyrdts, losses, label="tx")
    # plt.show()

    sns.lineplot(x="dxrdt", y="loss", data=df0)
    plt.show()
    sns.lineplot(x="dyrdt", y="loss", data=df0)
    plt.show()

    exit()

    if use_scaler:
        df_rock = pd.DataFrame(np.array([[xr0, yr0, zr0, dxrdt, dyrdt, dzrdt]]))
        df_rock_transformed = pd.DataFrame(scaler.transform(df_rock))
        xr0, yr0, zr0, dxrdt, dyrdt, dzrdt = df_rock_transformed.iloc[0].values

    learning_rate = 1e-2
    n = len(hailstones)
    epochs = 2
    total_losses = list()

    for _ in range(epochs):
        # print(xr0, yr0, zr0, dxrdt, dyrdt, dzrdt)
        loss = list()

        dloss_dxr0 = 0
        dloss_dyr0 = 0
        dloss_dzr0 = 0
        dloss_ddxrdt = 0
        dloss_ddyrdt = 0
        dloss_ddzrdt = 0

        for i in range(n):
            print("hailstone", i)
            x10, y10, z10, dx1dt, dy1dt, dz1dt = df.iloc[i].values
            if use_scaler:
                x10, y10, z10, dx1dt, dy1dt, dz1dt = df_transformed.iloc[i].values

            tx = (x10 - xr0) / (dxrdt - dx1dt) if (dxrdt - dx1dt) != 0 else np.nan
            ty = (y10 - yr0) / (dyrdt - dy1dt) if (dyrdt - dy1dt) != 0 else np.nan
            # tz = (z10 - zr0) / (dzrdt - dz1dt) if (dzrdt - dz1dt) != 0 else np.nan

            if np.isnan(tx):
                # tx = np.mean([ty, tz])
                tx = ty
            if np.isnan(ty):
                # ty = np.mean([tx, tz])
                ty = tx
            # if np.isnan(tz):
            #     tz = np.mean([tx, ty])

            loss.append((tx - ty) ** 2)  # + (ty - tz) ** 2 + (tz - tx) ** 2)
            print(
                i,
                tx,
                ty,
            )  # tz)
            # print(tx, ty, tz, loss)

            # determine partial derivatives of loss with respect to xr0, yr0, zr0, dxrdt, dyrdt, dzrdt
            # dloss_dxr0 += - 1 / (dxrdt - dx1dt) * (2 * tx - ty - tz) if (dxrdt - dx1dt) != 0 else 0
            # dloss_dyr0 += - 1 / (dyrdt - dy1dt) * (2 * ty - tx - tz) if (dyrdt - dy1dt) != 0 else 0
            # dloss_dzr0 += - 1 / (dzrdt - dz1dt) * (2 * tz - tx - ty) if (dzrdt - dz1dt) != 0 else 0
            # dloss_ddxrdt += -1 / (dxrdt - dx1dt) * tx * (2 * tx - ty - tz) if (dxrdt - dx1dt) != 0 else 0
            # dloss_ddyrdt += -1 / (dyrdt - dy1dt) * ty * (2 * ty - tx - tz) if (dyrdt - dy1dt) != 0 else 0
            # dloss_ddzrdt += -1 / (dzrdt - dz1dt) * tz * (2 * tz - tx - ty) if (dzrdt - dz1dt) != 0 else 0
            dloss_dxr0 += (
                -1 / (dxrdt - dx1dt) * (2 * tx - ty) if (dxrdt - dx1dt) != 0 else 0
            )
            dloss_dyr0 += (
                -1 / (dyrdt - dy1dt) * (2 * ty - tx) if (dyrdt - dy1dt) != 0 else 0
            )
            # dloss_dzr0 += - 1 / (dzrdt - dz1dt) * (2 * tz - tx - ty) if (dzrdt - dz1dt) != 0 else 0
            dloss_ddxrdt += (
                -1 / (dxrdt - dx1dt) * tx * (2 * tx - ty) if (dxrdt - dx1dt) != 0 else 0
            )
            dloss_ddyrdt += (
                -1 / (dyrdt - dy1dt) * ty * (2 * ty - tx) if (dyrdt - dy1dt) != 0 else 0
            )
            # dloss_ddzrdt += -1 / (dzrdt - dz1dt) * tz * (2 * tz - tx - ty) if (dzrdt - dz1dt) != 0 else 0

            print(
                "partial derivatives",
                dloss_dxr0,
                dloss_dyr0,
                dloss_dzr0,
                dloss_ddxrdt,
                dloss_ddyrdt,
                dloss_ddzrdt,
            )
            print("loss", loss)

        total_losses.append(np.mean(loss))

        # update rock starting values
        xr0 -= learning_rate * dloss_dxr0 / n
        yr0 -= learning_rate * dloss_dyr0 / n
        # zr0 -= learning_rate * dloss_dzr0 / n
        dxrdt -= learning_rate * dloss_ddxrdt / n
        dyrdt -= learning_rate * dloss_ddyrdt / n
        # dzrdt -= learning_rate * dloss_ddzrdt / n

    df_tmp = pd.DataFrame(np.array([[xr0, yr0, zr0, dxrdt, dyrdt, dzrdt]]))
    if use_scaler:
        df_tmp = pd.DataFrame(scaler.transform(df_tmp))

    return df_tmp.iloc[0].values


def analysis(content):
    hailstones = list()
    for line in content.split("\n"):
        data = list(map(int, re.findall(r"-?\d+", line)))
        hailstones.append(data)

    rock = [24, 13, 10, -3, 1, 2]

    # # get prime factors of all x10, y10, z10
    # for hailstone in hailstones:
    #     x10, y10, z10, *_ = hailstone
    #     divx = factorint(x10, multiple=True)
    #     divy = factorint(y10)
    #     divz = factorint(z10)
    #     print(x10, divx)
    #     print(y10, divy)
    #     print(z10, divz)
    #     print()

    # # plot dim1 vs dim2
    # times = np.arange(9)
    # fig, ax = plt.subplots(3, 3, sharex=True, sharey=True)
    # for t in times:
    #     for i, (_, dim1_0, dim2_0,  _, dim1_d, dim2_d) in enumerate([rock] + hailstones):
    #         if i == 0:
    #             marker = "o"
    #         else:
    #             marker = "x"
    #         dim1 = dim1_0 + dim1_d * times
    #         dim2 = dim2_0 + dim2_d * times
    #         ax[t // 3, t % 3].plot(dim1, dim2, label=f"{i}")
    #         ax[t // 3, t % 3].scatter([dim1_0 + dim1_d * t], [dim2_0 + dim2_d * t], marker=marker)
    # plt.legend()
    # plt.show()

    # statistics
    df = pd.DataFrame(hailstones)
    print(df.describe())


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

    # assert part2(SAMPLE) == 47

    # print(part2(SAMPLE))

    # analysis(SAMPLE)
    analysis(CONTENT)
    # print(part2(CONTENT))
