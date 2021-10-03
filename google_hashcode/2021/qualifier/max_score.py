from qualifier.input_data import InputData
import os

if __name__ == "__main__":
    THIS_PATH = os.path.abspath(os.path.dirname(__file__))
    directory = os.path.join(THIS_PATH, 'inputs')

    print(f'Optimal scores')
    for file_name in [
        'a.txt',  # instant
        'b.txt',  # 26s
        'c.txt',  # 17s
        'd.txt',  # 2m09s
        'e.txt',  # instant
        'f.txt',  # 4s
    ]:
        input_data = InputData(os.path.join(directory, file_name))
        score = 0

        for car in input_data.cars:
            penalty = sum([street.time for street in car.path[1:]])
            score += input_data.duration - penalty + input_data.bonus

        print(f'{file_name}: {score}')
