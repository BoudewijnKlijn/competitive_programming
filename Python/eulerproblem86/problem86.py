import math


def get_shortest_path_length_squared(a, b, c):
    """
    Observation: since c is always the largest or one of the largest inputs. Path3 is always shortest.
    No need to execute this function anymore
    """
    # path1 = squares[a] + squares[b+c]
    # path2 = squares[b] + squares[a+c]
    path3 = squares[c] + squares[a+b]

    # print(f"path1: {# path1}, path2: {path2}, path3: {path3}, min: {min([path1, path2, path3])}")

    # return min([path1, path2, path3])
    return path3


def for_one_m(m):
    """
    This function appears to run slow at first, but will speed up once you get closer to M.
    """
    shortest_path_with_integer_length = 0
    for a in range(1, m + 1):
        print(a)
        for b in range(a, m + 1):
            for c in range(b, m+1):
                # shortest_path_length_squared = get_shortest_path_length_squared(a, b, c)
                shortest_path_length_squared = squares[c] + squares[a+b]
                if shortest_path_length_squared in ints_squared:
                    shortest_path_with_integer_length += 1
    print(f"m: {m}, shortest_path_with_integer_length: {shortest_path_with_integer_length}")


def main():
    """
    m: 1818, shortest_path_with_integer_length: 1000457
    needs a few minutes to run.
    Try different approach. Create all integer solutions and then verify what M corresponds with 1 million.
    """
    shortest_path_with_integer_length = 0
    for m in range(1, M):
        print(f"Start. m: {m}")  # Show progress.

        for a in range(1, m+1):
            for b in range(a, m+1):
                c = m
                # shortest_path_length_squared = get_shortest_path_length_squared(a, b, c)
                shortest_path_length_squared = squares[c] + squares[a + b]
                if shortest_path_length_squared in ints_squared:
                    # print(f"a: {a}, b: {b}, c: {c}, length: {shortest_path_length_squared} {shortest_path_length_squared ** 0.5}")
                    shortest_path_with_integer_length += 1

        print(f"End. integer length paths: {shortest_path_with_integer_length}")  # Show progress.

        # Stop iteration.
        if shortest_path_with_integer_length > goal:
            print(f"Solution - m: {m}, shortest_path_with_integer_length: {shortest_path_with_integer_length}")
            break


def main2():
    t_list, t_set = create_pythagorean_triples()



def create_pythagorean_triples():
    """
    file:///C:/Users/Admin/Desktop/Pythagorean%20triple%20-%20Wikipedia.html
    """
    triples_set = set()
    triples = list()
    for n in range(1, 10):
        n_squared = n * n
        for m in range(n+1, 10):
            m_squared = m*m

            a = (m_squared - n_squared)
            b = 2 * m * n
            c = (m_squared + n_squared)
            k = 1
            while k*(a+b) < 2*M or k*c < M:
                ka = k * a
                kb = k * b
                kc = k * c

                k += 1

                triples_set.add(tuple(sorted([ka, kb, kc])))
                triples.append(tuple(sorted([ka, kb, kc])))

    print(len(triples_set))
    print(len(triples))
    return triples, triples_set


if __name__ == "__main__":
    M = 100
    goal = 10**6
    goal = 2000

    squares = {i: i ** 2 for i in range(2 * M + 2)}
    max_int = int(math.sqrt((2 * M) ** 2 + M ** 2)) + 1
    ints_squared = {i ** 2 for i in range(1, max_int)}

    # main()

    # for_one_m(1818)

    main2()
