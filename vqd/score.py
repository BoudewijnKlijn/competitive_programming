
# TODO validate here as well

def score(in_file=None, out_file=None):
    pizzas = []
    for idx, line in enumerate(open(in_file).readlines()):
        if idx > 0:
            ingredients = line.split()[1:]
            pizzas.append(ingredients)

    total_score = 0
    for idx, line in enumerate(open(out_file).readlines()):
        if idx > 0:
            pizza_indices = line.split()[1:]
            all_ingredients = set()

            for pizza_idx in pizza_indices:
                all_ingredients.update(pizzas[int(pizza_idx)])

            pizza_score = len(all_ingredients)**2
            total_score += pizza_score

    return total_score


# total = score(in_file="sample.in", out_file="sample.out")
# print(total)