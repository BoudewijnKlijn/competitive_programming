
# TODO validate here as well

def calculate_score(in_file=None, out_file=None, out_data=None):
    pizzas = []
    for idx, line in enumerate(open(in_file).readlines()):
        if idx > 0:
            ingredients = line.split()[1:]
            pizzas.append(ingredients)

    total_score = 0
    if out_data is not None:
        out_data = [len(out_data)] + [f'{entry[0]} {" ".join([str(x) for x in entry[1]])}' for entry in out_data]
    else:
        out_data = open(out_file).readlines()

    for idx, line in enumerate(out_data):
        if idx == 0:
            continue

        pizza_indices = line.split()[1:]
        all_ingredients = set()

        for pizza_idx in pizza_indices:
            all_ingredients.update(pizzas[int(pizza_idx)])

        pizza_score = len(all_ingredients)**2
        total_score += pizza_score

    return total_score


# total = score(in_file="sample.in", out_file="sample.out")
# print(total)