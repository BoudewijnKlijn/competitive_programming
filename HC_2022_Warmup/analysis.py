import os

from HC_2022_Warmup.pizza_demands import PizzaDemands

THIS_PATH = os.path.abspath(os.path.dirname(__file__))

if __name__ == '__main__':
    directory = os.path.join(THIS_PATH, 'input')
    files = [
        'a_an_example.in.txt',
        'b_basic.in.txt',
        'c_coarse.in.txt',
        'd_difficult.in.txt',
        'e_elaborate.in.txt',
    ]
    for problem_file in files:
        demands = PizzaDemands(os.path.join(directory, problem_file))
        unique_likes = set()
        unique_dislikes = set()
        for customer in demands.customers:
            unique_likes.update(customer.likes)
            unique_dislikes.update(customer.dislikes)

        print(f'{problem_file:<20}: {len(unique_likes):8d} likes, {len(unique_dislikes):8d} dislikes')