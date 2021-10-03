def multiply_and_reduce(number, multiply, mod):
    return (number * multiply) % mod


def main():
    exponent = 7830457
    number = 1
    step = 64
    for _ in range(exponent//step):
        number = multiply_and_reduce(number, 2 ** step, 10 ** 10)

    number = multiply_and_reduce(number, 2 ** (exponent % step), 10 ** 10)
    number = multiply_and_reduce(number, 28433, 10 ** 10)
    number += 1
    print(number)


if __name__ == "__main__":
    main()
