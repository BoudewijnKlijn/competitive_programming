import re
from functools import reduce


def load_data():
    with open(input_file, 'r') as f:
        data = f.read().strip()
    return data


def parse_data():
    ingredient_lines = list()
    allergen_lines = list()
    for line in data.split('\n'):
        ingredients_part, allergens_part = line.split(' (')
        ingredient_lines.append(set(ingredients_part.split(' ')))
        allergen_lines.append(set([a for a in re.findall(r'[a-z]+', allergens_part) if a != 'contains']))

    return ingredient_lines, allergen_lines


def part1():
    ingredient_lines, allergen_lines = parsed
    all_allergens = reduce(lambda x, y: x.union(y), allergen_lines)
    all_ingredients = reduce(lambda x, y: x.union(y), ingredient_lines)

    unmapped_allergens = set(all_allergens)
    mapped_allergens = dict()
    while unmapped_allergens:
        for allergen in unmapped_allergens:
            ingredients_when_allergen_present = [ingredients for ingredients, allergens in
                                                 zip(ingredient_lines, allergen_lines) if allergen in allergens]
            common_factors = reduce(lambda x, y: x.intersection(y), ingredients_when_allergen_present) - \
                             set(mapped_allergens.values())
            assert len(common_factors) > 0, 'must have a common factor'

            if len(common_factors) == 1:
                mapped_allergens[allergen] = list(common_factors)[0]
                unmapped_allergens -= {allergen}
                break

    ingredients_with_allergens = set(mapped_allergens.values())
    ingredients_without_allergens = all_ingredients - ingredients_with_allergens

    ans = 0
    for ingredients in ingredient_lines:
        for ingredient in ingredients:
            if ingredient in ingredients_without_allergens:
                ans += 1

    print('part2', ','.join(list(zip(*sorted(mapped_allergens.items())))[1]))

    return ans


def part2():
    pass


def main():
    a1 = part1()
    print(a1)

    a2 = part2()
    print(a2)


if __name__ == '__main__':
    input_file = 'input21.txt'
    data = load_data()
    parsed = parse_data()
    main()

    # t = timeit.Timer('part2_regex()', globals=globals())
    # n = 10
    # print(sum(t.repeat(repeat=n, number=1)) / n)
