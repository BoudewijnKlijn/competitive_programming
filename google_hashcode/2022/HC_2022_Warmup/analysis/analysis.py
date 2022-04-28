import json
import os
from collections import Counter
from HC_2022_Warmup.pizza_demands import PizzaDemands

THIS_PATH = os.path.abspath(os.path.dirname(__file__))

if __name__ == '__main__':
    directory = os.path.join(THIS_PATH, '../input')
    files = [
        'a_an_example.in.txt',
        'b_basic.in.txt',
        'c_coarse.in.txt',
        'd_difficult.in.txt',
        'e_elaborate.in.txt',
    ]
    n_most_common = 20

    for problem_file in files:
        demands = PizzaDemands(os.path.join(directory, problem_file))
        unique_likes = Counter()
        unique_dislikes = Counter()
        for customer in demands.customers:
            unique_likes.update(Counter(customer.likes))
            count_likes = Counter(unique_likes.values())
            unique_dislikes.update(Counter(customer.dislikes))
            count_dislikes = Counter(unique_dislikes.values())

        print(f'\n{problem_file}\n{len(unique_likes.keys()):8d} likes, {len(unique_dislikes.keys()):8d} dislikes')
        print(f'{n_most_common} most common LIKES: {unique_likes.most_common(n_most_common)}')
        print(f'{n_most_common} most common DISLIKES: {unique_dislikes.most_common(n_most_common)}')
        print(f'Occurrences of occurrences {json.dumps(dict(sorted(count_likes.items())), indent=4)}')
        print(f'Occurrences of occurrences {json.dumps(dict(sorted(count_dislikes.items())), indent=4)}')
